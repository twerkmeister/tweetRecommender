from __future__ import division
from math import log
import functools32  

from tweetRecommender.mongo import mongo
from tweetRecommender.tokenize import tokenize
   
LANGUAGE_COLLECTION = 'sample_tweets'

def score(tweet, webpage):
    tweet_terms = tweet['terms']
    news_terms = set(tokenize(webpage['content'].encode('utf-8')))                        
    return dirichlet(news_terms, tweet_terms)

score.fields = ['terms']

#|D| = number of terms in a tweets
#f(qi,d) =  frequencey of a term occur in a tweets
#|C| = total numbers terms in tweets collections
#c(qi) = frequency of a term in the tweets collection
#i term
#sum(log((f(qi,d) + miu * c(qi) / |C|)/(|D| + miu)))
miu = 1000  #dirichilet parameter typical 1,000< miu < 2,000  
def dirichlet(query, document):                        
    score = 0    
    for term in query:                    
        score += log((document.count(term) + miu * get_collection_term(term) / get_collection_vocab()) /
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
    return mongo.coll(LANGUAGE_COLLECTION).find({"terms" : {"$in" : [term]}}).count() + 1 #prevent 0 occurence in background
