from tweetRecommender.mongo import mongo
import tweetRecommender.web as webprocessor
import tweetRecommender.tweet as tweetprocessor

from tornado import gen
from tornado import ioloop

@gen.coroutine
def process_initial_subset(process_tweets=True, process_web=False):
    if process_tweets:
        tweets = mongo.db.tweets.find()
        while(yield tweets.fetch_next):
            process_tweet(tweets.next_object())

    if process_web:
        webpages = mongo.db.webpages.find()
        while(yield webpages.fetch_next):
            process_webpage(webpages.next_object())

def process_tweet(tweet):
    tweetprocessor.handle(tweet)

def process_webpage(webpage):
    webprocessor.handle(webpage.get('url'))

if __name__ == '__main__':
    import sys

    if len(sys.argv) not in (1, 3):
        sys.stderr.write("preprocessor [<process_tweets> <process_web>]")
        sys.exit(1)

    if len(sys.argv) == 1:
        process_initial_subset()
    else:
        process_initial_subset(sys.argv[1], sys.argv[2])

    ioloop.IOLoop.instance().start()