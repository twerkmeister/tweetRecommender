'''
Created on Apr 14, 2014

@author: easten
'''
from bson.objectid import ObjectId

from tweetRecommender.mongo import mongo
from tornado import ioloop
from tornado.httpclient import *
from tornado import gen

class RedirectResolver():

    def __init__(self):
        AsyncHTTPClient.configure("tornado.simple_httpclient.SimpleAsyncHTTPClient", max_clients=100)
        self.http_client = AsyncHTTPClient()

    @gen.coroutine
    def find_redirect(self, url):
        redirect = yield mongo.db.redirects.find_one({"from" : url})
        if redirect:
            raise gen.Return(redirect["to"])
        else:
            raise gen.Return(None)

    @gen.coroutine
    def resolve_redirect(self, url):
        print "resolving redirect"
        request = HTTPRequest(url=url, connect_timeout=10.0, request_timeout=10.0)
        try:
            response = yield self.http_client.fetch(request)
        except HTTPError as e:
            if e.code == 599:
                #handle timeout
                pass
            raise gen.Return(None)
        raise gen.Return(response.effective_url)

    @gen.coroutine
    def handle(self, url, _id):
        redirect = yield self.find_redirect(url)
        if not redirect:
            redirect = yield self.resolve_redirect(url)
            if redirect:
                mongo.db.redirects.insert({'from': url, 'to': redirect.encode("utf-8")})
        if redirect:
            mongo.db.tweets.update({'_id': ObjectId(_id)},
                                   {'$addToSet': {'full_urls': redirect.encode("utf-8")}}, 
                                   True)            
            raise gen.Return(redirect)
        else:
            raise gen.Return(None)

    @gen.coroutine
    def handle_tweet_id(self, _id):
        tweet = yield mongo.by_id('tweets', _id)
        self.handle_tweet(tweet)

    def handle_tweet(self, tweet):
        for url in tweet["urls"]:
            self.handle(url, tweet['_id'])

resolver = RedirectResolver()
def main():
    resolver.handle_tweet_id("52adb77a00323226c3b871dc")

@gen.coroutine
def handle(url, _id):
    redirect = yield resolver.handle(url, _id)
    raise gen.Return(redirect)

if __name__ == '__main__':
    main()
    #ioloop.IOLoop.instance().start()
