from mongoconnector import mongo
import sys

def gather(url):
  webpage_tweets_index = mongo.db.webpages_tweets
  tweets = mongo.db.tweets

  query = {"url": url}
  webpage_tweets_entry = webpage_tweets_index.find_one(query)
  if bool(webpage_tweets_entry):
    tweets = [tweets.find_one({"_id": tweet_id}) for tweet_id in webpage_tweets_entry.tweets]
    return tweets
  else:
    return []

def rank(tweets):
  def score(tweet):
    return tweet["user"]["followers_count"]

  ranked_tweets = [(tweet, score(tweet)) for tweet in tweets]
  ranked_tweets.sort(key=lambda pair: pair[1], reverse=True)
  return ranked_tweets

def print_rank(ranked_tweets):
  print("Ranking:")
  for tweet,score in ranked_tweets:
    print("text: %s / score: %d" % (tweet.text, score))


if __name__=="__main__":

  if len(sys.argv) < 2:
    print("please provide a url")
    sys.exit(1)

  tweets = gather(sys.argv[1])
  ranked_tweets = rank(tweets)
  print_rank(ranked_tweets)



