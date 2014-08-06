from __future__ import division
from math import log
import functools32  

from tweetRecommender.mongo import mongo
from tweetRecommender.tokenize import tokenize

from collections import defaultdict
   
DISPLAY_NAME = "Text similarity"

LANGUAGE_COLLECTION = 'sample_tweets'
COLLECTION_STATISTICS_COLLECTION = "collection_statistics"


def readCollectionStatistics():
  counts = defaultdict(int)
  overall_size = 0
  for term_count in mongo.coll(COLLECTION_STATISTICS_COLLECTION).find():
      counts[term_count["term"]] += term_count["count"]
      overall_size += term_count["count"]
  return counts, overall_size

collection_stats, overall_size = readCollectionStatistics()

def score(tweet, webpage):
    tweet_terms = tweet['terms']
    news_terms = tokenize(webpage['content'].encode('utf-8'))                        
    return dirichlet(tweet_terms, news_terms)

score.fields = ['terms']

#|D| = number of query terms in a tweets
#f(qi,d) =  frequencey of a query term occur in a tweets
#|C| = total numbers terms in tweets collections
#c(qi) = frequency of a term in the tweets collection
#i term
#sum(log((f(qi,d) + miu * c(qi) / |C|)/(|D| + miu)))
miu = 2000  #dirichilet parameter typical 1,000< miu < 2,000  
def dirichlet(query, document):                        
    score = 0    
    for term in query:                    
        score += log((float(document.count(term)) + miu * collection_stats[term] / overall_size) /
                        (len(document) + miu))             
    return score

#a parameter (0 means no smoothing)
#sum(log(((1-a)*f(qi,d)/|D|) + (a * c(qi) / |C|)))
a = 0.7 #0.3 for short query and 0.7 for long query
def jelinek_mercer(query, document):                        
    score = 0            
    for term in query:        
        score += log((1-a)*document.count(term) / len(document) + 
                     a * get_collection_term(term) / get_collection_vocab())
    return score

@functools32.lru_cache() 
def get_collection_vocab():
    return mongo.coll(LANGUAGE_COLLECTION).aggregate([{ "$unwind" : "$terms" }, 
                                                      { "$group": {  "_id": "null",
                                                            "total": { "$sum":1 } } } ])["result"][0]["total"];
@functools32.lru_cache(1000)                                                             
def get_collection_term(term):
    return mongo.coll(LANGUAGE_COLLECTION).find({"terms" : {"$in" : [term]}}).count() 
>>>>>>> 051f6b0e8e8a458d337f2ff356d0ad9682ca2138
