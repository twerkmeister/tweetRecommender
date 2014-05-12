from __future__ import division

def score(tweet, tokenized_webpage):
    tweet_terms = set(tweet['terms'])
    news_terms = set(tokenized_webpage)
    intersection = news_terms.intersection(tweet_terms)
    score = len(intersection) / len(tweet_terms)
    print score
    return score
