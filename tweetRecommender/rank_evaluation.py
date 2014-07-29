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
    value = mongo.coll(CACHED_RESULTS_COLLECTION).find_one({"$and" : [{"query_url" : query_url},{"eval.map" : {"$exists" : "true"}}]})
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
                                tweets_ref=TWEETS_SUBSAMPLE, webpages_ref=WEBPAGES_SUBSAMPLE, limit=10)                    
            for _, tweet in ranker_result:
                position += 1                    
                if (ObjectId(tweet["_id"]) in collections):                                
                    relevants += 1
                    precisions.append(relevants/position)
            meanap = sum(precisions)/relevants
            map_dict[ranker] = meanap                                                       
            print ("evaluation algorithm: %s" % ranker)
            print ("number of relevant tweets: %s" % relevants)
            print ("Mean Average Precision: %f \n" % meanap)
        mongo.coll(CACHED_RESULTS_COLLECTION).update({"query_url":query_url},{"$set": { "eval" : {"map" : map_dict }}})
    return map_dict

def evaluate_collections():
    ranks = dict()        
    count = 0
    for webpage in mongo.coll(CACHED_RESULTS_COLLECTION).find({},{"query_url":1}):                     
        count += 1        
        value = 0                        
        print "evaluate webpage: ", count
        ranks_dict = calculate_MAP(webpage["query_url"])                                
        for ranker in ranks_dict.keys():
            if ranker in ranks:
                value = ranks.get(ranker)
            ranks[ranker] = ranks_dict[ranker] + value                                                                                                    
    for ranker in EVALUATION_RANKERS:        
        print "Average MAP %s : %f" % (ranker, (ranks[ranker]/count))
                      
if __name__ == '__main__':
    evaluate_collections()         