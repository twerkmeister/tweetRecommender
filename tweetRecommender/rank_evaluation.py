from __future__ import division 
from tweetRecommender.mongo import mongo
from tweetRecommender.query import run
from bson import ObjectId
import functools32

TWEETS_COLLECTION = 'tweets'
WEBPAGES_COLLECTION = 'webpages'
TWEETS_SUBSAMPLE = 'sample_tweets'
WEBPAGES_SUBSAMPLE = 'sample_webpages'

EVALUATION_GATHERER = "terms"
EVALUATION_FILTERS = []
EVALUATION_RANKERS = ['lda_cossim', 'language_model', 'text_overlap, normalized_follower_count']
CACHED_RESULTS_COLLECTION = 'evaluation_cache_advanced'

@functools32.lru_cache()
def get_evaluated_collection(url):
    value = []
    collection = mongo.coll("evaluation").aggregate([{"$match" : { "webpage" : url}},
                                               {"$group": {
        "_id": "$tweet",
        "positive": {"$sum": {"$cond": {"if": {"$eq": ["$rating", +1]}, "then": 1, "else": 0}}},
        "negative": {"$sum": {"$cond": {"if": {"$eq": ["$rating", -1]}, "then": 1, "else": 0}}},
    }}])["result"]
    for tweet in collection:
        if tweet["positive"] > tweet["negative"]:
            value.append(ObjectId(tweet["_id"]))
    return set(value)    

def calculate_MAP(query_url):    
    collections = get_evaluated_collection(query_url)                        
    map_dict = dict()                
    value = mongo.coll(CACHED_RESULTS_COLLECTION).find_one({"$and" : [{"query_url" : query_url},{"eval.mapk" : {"$exists" : "true"}}]})
    if value:
        map_dict = dict(value["eval"]["map"])
    else: 
        for ranker in EVALUATION_RANKERS:                
            relevants = 0
            position = 0 
            precisions = []
            rankers = ranker.split(',')
            ranker_result = run(url=query_url, gatherer=EVALUATION_GATHERER, rankers=rankers,
                                filters=EVALUATION_FILTERS, fields=['user.screen_name', 'created_at', 'text'],
                                tweets_ref=TWEETS_SUBSAMPLE, webpages_ref=WEBPAGES_SUBSAMPLE, limit = None)                    
            for _, tweet in ranker_result:
                position += 1                    
                if (ObjectId(tweet["_id"]) in collections):                                
                    relevants += 1
                    precisions.append(relevants/position)
            meanap = sum(precisions)/relevants
            map_dict[ranker] = meanap                                                                           
        mongo.coll(CACHED_RESULTS_COLLECTION).update({"query_url":query_url},{"$set": { "eval.map" : map_dict }})
    return map_dict

def calculate_p_at(query_url, positions):    
    collections = get_evaluated_collection(query_url)                        
    map_dict = dict()                
    value = mongo.coll(CACHED_RESULTS_COLLECTION).find_one({"$and" : [{"query_url" : query_url},{"eval.p10" : {"$exists" : "true"}}]})
    if value:
        map_dict = dict(value["eval"]["p10"])
    else: 
        for ranker in EVALUATION_RANKERS:                
            relevants = 0
            position = 0     
            precision_at = 0        
            rankers = ranker.split(',')
            ranker_result = run(url=query_url, gatherer=EVALUATION_GATHERER, rankers=rankers,
                                filters=EVALUATION_FILTERS, fields=['user.screen_name', 'created_at', 'text'],
                                tweets_ref=TWEETS_SUBSAMPLE, webpages_ref=WEBPAGES_SUBSAMPLE, limit=10)
            print "lenghtnya adalah: " , len(ranker_result)                    
            for _, tweet in ranker_result:
                position += 1                    
                if (ObjectId(tweet["_id"]) in collections):                                
                    relevants += 1  
                if position == positions:
                    precision_at = relevants/position
                    break;                    
            map_dict[ranker] = precision_at
        mongo.coll(CACHED_RESULTS_COLLECTION).update({"query_url":query_url},{"$set": { "eval.p10" : map_dict }})
    return map_dict

def evaluate_collections():
    rank_map = dict()  
    rank_pap = dict()      
    count = 0
    for webpage in mongo.coll(CACHED_RESULTS_COLLECTION).find({},{"query_url":1}):                     
        count += 1        
        value = 0                                
        print "\nevaluated article: ", count
        ranks_dict = calculate_p_at(webpage["query_url"], 10)
        for key in ranks_dict.keys():
            print ("precision at 10 %s : %f" % (key,ranks_dict[key]))                        
            if key in rank_pap:
                value = rank_pap.get(key)
            rank_pap[key] = ranks_dict[key] + value                
        value = 0  
        ranks_dict = calculate_MAP(webpage["query_url"])                                    
        for key in ranks_dict.keys():
            print ("AP %s : %f" % (key,ranks_dict[key]))                        
            if key in rank_map:
                value = rank_map.get(key)
            rank_map[key] = ranks_dict[key] + value                
    print "\n"                                                                                                
    for ranker in EVALUATION_RANKERS:        
        print "Average MAP %s : %f" % (ranker, (rank_map[ranker]/count))
        print "Average precision @10 %s : %f" % (ranker, (rank_pap[ranker]/count))
                      
if __name__ == '__main__':
    evaluate_collections()         