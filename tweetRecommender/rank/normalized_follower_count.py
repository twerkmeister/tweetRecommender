from __future__ import division

def score(tweet, webpage):
    return tweet["user"]["followers_count"] / tweet["user"]["statuses_count"]

FIELDS = ['user.followers_count', 'user.statuses_count']
