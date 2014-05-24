def score(tweet, webpage):
    return tweet["user"]["followers_count"]

score.fields = ['user.followers_count']
