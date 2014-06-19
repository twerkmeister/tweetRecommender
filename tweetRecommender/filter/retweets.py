DISPLAY_NAME = "No retweets"

def filter(webpage):
    return {'retweeted_status': {'$exists': 0}}
