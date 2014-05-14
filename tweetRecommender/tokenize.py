from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from tweetRecommender.mongo import mongo
from tweetRecommender import tweetfilter
import functools32

ps = PorterStemmer()

@functools32.lru_cache()
def get_stopwords():
    stops = stopwords.words('english')
    stops.extend(["'re", "n't", "'s"])
    return stops

def get_terms(text):
    return list(set(tokenize_tweets(text)))

@functools32.lru_cache()
def tokenize(text):
    text = tweetfilter.clean_tweet(text)
    return [ps.stem(w) for w in word_tokenize(text)
            if not w in get_stopwords()]

def handle(tweet, bulk):
    text = tweet["text"]
    tweet_id = tweet["_id"]
    tokens = list(set(tokenize_tweets(text.encode("utf-8"))))
    bulk.find({'_id': tweet_id}).update({'$set': {'terms': tokens}})

if __name__ == '__main__':
    bulk = mongo.db.sample_tweets.initialize_unordered_bulk_op()
    for tweet in mongo.db.sample_tweets.find():
        handle(tweet, bulk)
    bulk.execute()
