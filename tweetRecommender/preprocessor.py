from tweetRecommender.mongo import mongo
import tweetRecommender.web as webprocessor
import tweetRecommender.tweet as tweetprocessor

import multiprocessing as mp

class TweetWorker (mp.Process):
	def __init__(self, queue):
		mp.Process.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			tweet = self.queue.get()
			process_tweet(tweet)


def process_initial_subset(process_tweets=True, process_web=False):
    if process_tweets:
    	q = mp.Queue(1000)

    	workers = []
    	for i in range(mp.cpu_count()):
    		w = TweetWorker(q)
    		w.start()
    		workers.append(w)

        tweets = mongo.db.tweets.find(timeout=False)

        for i, tweet in enumerate(tweets):
        	if (i%10000) == 0:
        		print i
        	q.put(tweet)

        for w in workers:
        	w.join()


        

    if process_web:
        webpages = mongo.db.webpages.find()
        for webpage in webpages:
            process_webpage(webpage)

def process_tweet(tweet):
	tweetprocessor.handle(tweet)

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

