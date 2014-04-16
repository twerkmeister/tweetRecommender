from tweetRecommender.mongo import mongo
import sys

def gather(url):
    index = mongo.db.webpages_tweets
    tweets = mongo.db.tweets

    query = {"url": url}
    index_entry = index.find_one(query)
    tweet_ids = index_entry['tweets'] if index_entry else []

    tweets = [tweets.find_one({"_id": tweet_id})
              for tweet_id in tweet_ids]
    return tweets

def rank(tweets):
    def score(tweet):
        return tweet["user"]["followers_count"]

    ranked_tweets = [(tweet, score(tweet)) for tweet in tweets]
    ranked_tweets.sort(key=lambda pair: pair[1], reverse=True)
    return ranked_tweets


def main(uri):
    tweets = gather(uri)
    ranked_tweets = rank(tweets)
    print("Ranking:")
    for tweet, score in ranked_tweets:
        print("[%.2f] text: %s" % (score, tweet.text))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please provide a url")
        sys.exit(1)
    main(sys.argv[1])
