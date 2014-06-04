from __future__ import division

from tweetRecommender.tokenize import tokenize

def score(tweet, webpage):
    tweet_terms = set(tweet['terms'])
    news_terms = set(tokenize(webpage['content'].encode('utf-8')))
    intersection = news_terms.intersection(tweet_terms)
    score = len(intersection) / (len(tweet_terms) + len(news_terms))
    return score

score.fields = ['terms']
