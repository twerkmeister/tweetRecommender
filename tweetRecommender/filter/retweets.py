def filter():
    return {'retweeted_status': {'$exists': 0}}
