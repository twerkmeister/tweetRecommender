from tweetRecommender.mongo import mongo
from collections import defaultdict

TWEET_COLLECTION="sample_tweets"

def run():
  counts = defaultdict(int)
  for tweet in mongo.coll(TWEET_COLLECTION).find():
    for term in tweet["terms"]:
      counts[term] += 1

  background_coll = mongo.coll("collection_statistics")
  for term, count in counts.items():
    background_coll.insert({"term": term, "count": count})

if __name__ == "__main__":
  run()