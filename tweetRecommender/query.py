from tweetRecommender.mongo import mongo
import tweetRecommender.querybaseline as q
import sys

def gather(url):
    return q.gather(url)

def rank(tweets, news_terms):
    return q.rank(tweets, news_terms)

def query(uri):
    tweets, news_terms = gather(uri)
    ranked_tweets = rank(tweets, news_terms)
    return ranked_tweets

def main(uri):
    ranked_tweets = query(uri)
    print("Ranking:")
    for score, tweet in ranked_tweets:
        print("[%.6f] text: %s" % (score, tweet["text"].encode("utf-8")))


if __name__ == "__main__":  
    if len(sys.argv) < 2:
        print("please provide a url")
        sys.exit(1)
    main(sys.argv[1])
