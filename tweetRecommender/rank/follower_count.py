def score(tweet):
    return tweet["user"]["followers_count"]

FIELDS = ['user.followers_count']
