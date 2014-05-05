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

#thanks to http://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
def strip_regex(word):       
    #return re.sub(r'[^\w\s]','',word)  #remove word only
    return re.sub(r'[^a-zA-Z\s]',None,word) #remove number as well

def strip_trans(s):
    return s.translate(None, string.punctuation)

def tokenize_tweets(text):    
    text = tweetfilter.clean_tweet(text)    
    return [ps.stem(w) for s in sent_tokenize(text) for w in word_tokenize(s)]

def handle(text, tweet_id):    
    tokens = list(Set([strip_trans(token) for token in tokenize_tweets(text.encode("utf-8")) if token not in get_stopwords()]))
    tokens = filter(None, tokens)     
    mongo.db.sample_tweets.update({'_id': ObjectId(tweet_id)}, 
                                  { '$set': {'terms':  tokens } })
    print "update: ", tokens
    
if __name__ == '__main__':
    for tweet in mongo.db.sample_tweets.find():
        handle(tweet["text"], tweet["_id"])

    