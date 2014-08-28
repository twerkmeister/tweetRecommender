from tweetRecommender.mongo import mongo
from tweetRecommender.tokenize import tokenize
from collections import defaultdict

TWEET_COLLECTION="sample_tweets"
WEBPAGE_COLLECTION="sample_webpages"

def run_tweets():
  counts = defaultdict(int)
  for tweet in mongo.coll(TWEET_COLLECTION).find():
    for term in tweet["terms"]:
      counts[term] += 1

  background_coll = mongo.coll("collection_statistics_tweets")
  for term, count in counts.items():
    background_coll.insert({"term": term, "count": count})
    
def run_webpage():
  counts = defaultdict(int)  
  for webpage in mongo.coll(WEBPAGE_COLLECTION).find():      
      news_terms = tokenize(webpage['content'].encode('utf-8'))
      for term in news_terms:      
          counts[term] += 1

  background_coll = mongo.coll("collection_statistics_webpages")
  for term, count in counts.items():
    background_coll.insert({"term": term, "count": count})    

if __name__ == "__main__":
  run_webpage()