from tweetRecommender.config import config

def check(tweet):
    return check_size(tweet.text) and check_author_credibility(tweet)


def check_size(text):
	cleaned = clean_tweet(text)
	return len(cleaned) >= config['tweet_min_length']

def clean_tweet(text):
	#XXX remove hashtags and artifacts
	return text

def check_author_credibility(tweet):
	#XXX check #followers etc.
	return True
