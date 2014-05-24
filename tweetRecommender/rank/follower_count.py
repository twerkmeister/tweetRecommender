def score(tweet, webpage):
    return tweet["user"]["followers_count"]

FIELDS = ['user.followers_count']
