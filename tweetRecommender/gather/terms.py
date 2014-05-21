from __future__ import division

from tweetRecommender.tokenize import get_terms

def gather(webpage):
    terms = get_terms(webpage['content'].encode('utf-8'))
    return {'terms': {'$in': terms}}
