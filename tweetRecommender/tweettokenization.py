import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from tweetRecommender.mongo import mongo
from bson.objectid import ObjectId
import functools32
import tweetfilter
import string
import re
from sets import Set
 
ps = PorterStemmer()

def get_stopwords():
    stops = stopwords.words('english')
    stops.extend(["'re", "n't", "'s"])    
    return stops  

@functools32.lru_cache()
def tokenize_tweets(text):    
    text = tweetfilter.clean_tweet(text)    
    return [ps.stem(w) for w in word_tokenize(text) if not w in get_stopwords()]    

def handle(tweet, bulk):
    text = tweet["text"]
    tweet_id = tweet["_id"]
    tokens = list(Set([token for token in tokenize_tweets(text.encode("utf-8"))]))    
    bulk.find({'_id': tweet_id}).update({'$set': {'terms': tokens}})
    print "update: ", tokens
    
if __name__ == '__main__':
    bulk = mongo.db.sample_tweets.initialize_unordered_bulk_op()
    for tweet in mongo.db.sample_tweets.find():
        handle(tweet, bulk)
    bulk.execute()
