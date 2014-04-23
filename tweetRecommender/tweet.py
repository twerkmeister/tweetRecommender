from tweetRecommender import resolution
from tweetRecommender import web
from tornado import gen
import sys

counter = 0

@gen.coroutine
def handle(tweet):
    # URI matching
    _id = tweet['_id']
    for url in tweet['urls']:
        redirect = yield resolution.handle(url, _id)
        global counter 
        counter += 1
        sys.stdout.write("\rprogress: %s " % counter)
        sys.stdout.flush()
        if(redirect):
          web.handle(redirect)
