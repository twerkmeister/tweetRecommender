import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from tweetRecommender.mongo import mongo
from bson.objectid import ObjectId
import tweetfilter
import string
import re
from sets import Set
 
ps = PorterStemmer()

def get_stopwords():
    stops = stopwords.words('english')
    stops.extend(["'re", "n't", "'s"])    
    return stops  

def tokenize_tweets(text):    
    text = tweetfilter.clean_tweet(text)    
    return [ps.stem(w) for w in word_tokenize(text) if not w in get_stopwords()]    

def handle(text, tweet_id):    
    tokens = list(Set([token for token in tokenize_tweets(text.encode("utf-8"))]))    
    mongo.db.sample_tweets.update({'_id': ObjectId(tweet_id)}, 
                                  { '$set': {'terms':  tokens } })
    print "update: ", tokens
    
if __name__ == '__main__':
    for tweet in mongo.db.sample_tweets.find():
        handle(tweet["text"], tweet["_id"])

    