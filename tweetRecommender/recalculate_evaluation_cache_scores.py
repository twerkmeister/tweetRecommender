
from tweetRecommender.mongo import mongo
from tweetRecommender.query import CACHED_RESULTS_COLLECTION
from tweetRecommender.query import WEBPAGES_SUBSAMPLE
from tweetRecommender.query import EVALUATION_RANKERS
from tweetRecommender import machinery

cache_collection = mongo.coll(CACHED_RESULTS_COLLECTION)
webpages_collection = mongo.coll(WEBPAGES_SUBSAMPLE)

for cached_result in cache_collection.find():
    webpage = webpages_collection.find_one({"url": cached_result["query_url"]})
    for tweet in cached_result["tweet_list"]:
        for index,ranker in enumerate(EVALUATION_RANKERS):
            score_func = machinery.load_component(machinery.SCORE_PACKAGE, ranker, machinery.SCORE_METHOD)
            tweet["scores"][index][ranker] = score_func(tweet["tweet"], webpage)
    cache_collection.save(cached_result)
