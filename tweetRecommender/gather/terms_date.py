from __future__ import division

from tweetRecommender.tokenize import get_terms
from datetime import datetime, timedelta

STANDARD_DEVIATION_HOURS=43

def gather(webpage, tweets, webpages):
    terms = get_terms(webpage['content'].encode('utf-8'))
    lower_bound = webpage['created_at'] - timedelta(hours = STANDARD_DEVIATION_HOURS)
    upper_bound = webpage['created_at'] + timedelta(hours = STANDARD_DEVIATION_HOURS)
    tweets = tweets.find({'terms': {'$in': terms}, 'created_at': {"$gt": lower_bound}, 'created_at': {"$lt": upper_bound}})
    return tweets
