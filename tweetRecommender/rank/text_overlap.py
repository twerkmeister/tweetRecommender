from __future__ import division

from tweetRecommender.tweettokenization import tokenize_tweets as tokenize

def score(tweet, webpage):
    tweet_terms = set(tweet['terms'])
    news_terms = set(tokenize(webpage['content'].encode('utf-8')))
    intersection = news_terms.intersection(tweet_terms)
    score = len(intersection) / len(tweet_terms)
    return score
