from tweetRecommender.mongo import mongo
import tweetRecommender.web as webprocessor
import tweetRecommender.resolution as tweetprocessor

def process_initial_subset(process_tweets=True, process_web=False):
    if process_tweets:
        tweets = mongo.db.tweets.find()
        for tweet in tweets:
            process_tweet(tweet)

    if process_web:
        webpages = mongo.db.webpages.find()
        for webpage in webpages:
            process_webpage(webpage)

def process_tweet(tweet):
    tweetprocessor.handle_mongo(tweet.get('_id'))

def process_webpage(webpage):
    webprocessor.handle(webpage.get(url))

