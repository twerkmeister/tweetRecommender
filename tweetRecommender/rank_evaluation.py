from __future__ import division 
from tweetRecommender.mongo import mongo
from tweetRecommender.query import run
from bson import ObjectId

TWEETS_COLLECTION = 'tweets'
WEBPAGES_COLLECTION = 'webpages'
TWEETS_SUBSAMPLE = 'sample_tweets'
WEBPAGES_SUBSAMPLE = 'sample_webpages'

EVALUATION_GATHERER = "terms"
EVALUATION_FILTERS = []
EVALUATION_RANKERS = ['lda_cossim', 'language_model', 'text_overlap, normalized_follower_count']
CACHED_RESULTS_COLLECTION = 'evaluation_cache_advanced'

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

def evaluate_rank(query_url):    
    collections = get_evaluated_collection(query_url)
    ranks = dict()    
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
        print ("evaluation algorithm: %s" % ranker)
        print ("number of relevant tweets: %s" % relevants)
        print ("Mean Average Precision: %f" % (sum(precisions)/relevants))                    

if __name__ == '__main__':    
    evaluate_rank("http://www.washingtonpost.com/blogs/worldviews/wp/2013/08/06/some-girls-have-been-married-60-times-by-the-time-they-turn-18/")