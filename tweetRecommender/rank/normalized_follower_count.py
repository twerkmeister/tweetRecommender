from __future__ import division

DISPLAY_NAME = "User popularity"

def score(tweet, webpage):
    statuses = tweet["user"]["statuses_count"]
    if not statuses:
        statuses = 1
    return tweet["user"]["followers_count"] / statuses

score.fields = ['user.followers_count', 'user.statuses_count']
