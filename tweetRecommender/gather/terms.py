from __future__ import division

from tweetRecommender.tweettokenization import tokenize_tweets as tokenize

def gather(webpage, tweets, webpages):
    tokens = tokenize(webpage['content'].encode('utf-8'))
    terms = list(set(tokens))
    terms = terms[:1]

    tweets = tweets.find({'terms': {'$in': terms}})
    return tweets
