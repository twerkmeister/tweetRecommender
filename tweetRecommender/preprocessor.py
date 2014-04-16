from tweetRecommender.mongo import mongo
import tweetRecommender.web as webprocessor
import tweetRecommender.resolution as tweetprocessor

import multiprocessing as mp

def process_initial_subset(process_tweets=True, process_web=False):
    if process_tweets:
    	q = mp.Queue()
    	p = mp.Process(target=process_tweet, args=(q,))
    	p.start()
        tweets = mongo.db.tweets.find()
        for tweet in tweets:
            q.put(tweet.get('_id'))
        p.join()

    if process_web:
        webpages = mongo.db.webpages.find()
        for webpage in webpages:
            process_webpage(webpage)

def process_tweet(tweet_queue):
	tweet_id = tweet_queue.get()
    tweetprocessor.handle_mongo(tweet_id)

def process_webpage(webpage):
    webprocessor.handle(webpage.get('url'))

if __name__ == '__main__':
	import sys

	if ((len(sys.argv) != 1) and (len(sys.argv) != 3)):
		print "preprocessor [<process_tweets> <process_web>]"
		sys.exit(1)

	if len(sys.argv) == 1:
		process_initial_subset()
	if len(sys.argv) == 3:
		process_initial_subset(sys.argv[1], sys.argv[2])

