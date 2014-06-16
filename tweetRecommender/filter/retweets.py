def filter(webpage):
    return {'retweeted_status': {'$exists': 0}}
