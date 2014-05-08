from tweetRecommender.mongo import mongo
import tweetRecommender.querybaseline as q
import sys

def gather(url):
    return q.gather(url)

def rank(tweets):
    return q.rank(tweets)

def query(uri):
    tweets = gather(uri)
    ranked_tweets = rank(tweets)
    return ranked_tweets

def main(uri):
    ranked_tweets = query(uri)
    print("Ranking:")
    for tweet, score in ranked_tweets:
        print("[%.2f] text: %s" % (score, tweet["text"].encode("utf-8")))


if __name__ == "__main__":  
    if len(sys.argv) < 2:
        print("please provide a url")
        sys.exit(1)
    main(sys.argv[1])
