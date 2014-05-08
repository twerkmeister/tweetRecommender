from __future__ import division
from tweetRecommender.mongo import mongo
import tweettokenization
from sets import Set
from Queue import PriorityQueue 
import sys

def gather(url):
    webpages_coll = mongo.db.sample_webpages
    tweets_coll = mongo.db.sample_tweets
    query = {"url" : url}
    webpage = webpages_coll.find_one(query)
    news_terms = Set(tweettokenization.tokenize_tweets(webpage["content"].encode("utf-8")));
    tweets = tweets_coll.find({ "hashtags": { "$in": list(news_terms) } })
    return (webpage, tweets, news_terms)                                        

def rank(webpage, tweets, news_terms, topK=10):        
    queue = PriorityQueue(topK)        
    def calculate_score(tweet):
        tweet_terms = Set(tweet["terms"])
        intersection = news_terms.intersection(tweet_terms)        
        union = news_terms.union(tweet_terms)   
        score = len(intersection) / len(union)        
        return score    
    for tweet in tweets:        
        score = calculate_score(tweet)
        if not queue.full():
            queue.put((score, tweet)) 
        elif (score > queue.queue[0][0]):            
            queue.get()                
            queue.put((score, tweet))
    
    queue.queue.sort(reverse=True)
    return queue.queue


def main(uri):    
    webpage,tweets, news_terms = gather(uri)
    ranked_tweets = rank(webpage, tweets, news_terms)
    print("Ranking:")    
    for score, tweet in ranked_tweets:        
        print("[%.2f] text: %s" % (score, tweet["text"].encode("utf-8")))


if __name__ == "__main__":        
    if len(sys.argv) < 2:     
        print("please provide a url")
        sys.exit(1)
    main(sys.argv[1])
