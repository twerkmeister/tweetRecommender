from tweetRecommender import resolution
from tweetRecommender import web
from tornado import gen

@gen.coroutine
def handle(tweet):
    # URI matching
    _id = tweet['_id']
    for url in tweet['urls']:
        redirect = yield resolution.handle(url, _id)
        if(redirect):
          web.handle(redirect)
