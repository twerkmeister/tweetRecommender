from __future__ import division

from tweetRecommender.tweettokenization import get_terms

def gather(webpage, tweets, webpages):
    terms = get_terms(webpage['content'].encode('utf-8'))
    tweets = tweets.find({'terms': {'$in': terms}})
    return tweets
