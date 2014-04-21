from tweetRecommender import resolution
from tweetRecommender import web

def handle(tweet):
    # URI matching
    _id = tweet['_id']
    for url in tweet['urls']:
        redirect = resolution.handle(url, _id)

        web.handle(redirect)
