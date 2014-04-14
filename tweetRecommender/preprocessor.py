from mongoconnector import mongo
import tweetRecommender.web as webprocessor

def process_initial_subset(processTweets = True, processWeb = False):
	if processTweets:
		tweets = mongo.db.tweets.find()
		for tweet in tweets:
			process_tweet(tweet)

	if processWeb:
		webpages = mongo.db.webpages.find()	
		for webpage in webpages:
			process_webpage(webpage)

def process_tweet(tweet):
	#do stuff

def process_webpage(webpage):
	webprocessor.handle(webpage.get(url))

