from __future__ import division

DISPLAY_NAME = "User popularity"

def score(tweet, webpage):
    return tweet["user"]["followers_count"] / (
           tweet["user"]["statuses_count"] + 1)

score.fields = ['user.followers_count', 'user.statuses_count']
