from __future__ import division

from tweetRecommender.tokenize import tokenize
from math import log


#|D| = number of terms in tweets
#f(qi,d) =  frequencey of a term in tweets
#miu = dirichilet parameter typical 1,000< miu < 2,000
#|C| = number of terms in news article
#c(qi) = frequency of a term in the news article
#i term
#sum(log((f(qi,d) + miu * c(qi) / |C|)/(|D| + miu)))
miu = 2000    

def score(tweet, webpage):
    tweet_terms = tweet['terms']
    news_terms = tokenize(webpage['content'].encode('utf-8'))            
    log_sum = 0
    news_terms_total = len(news_terms);
    tweet_terms_total = len(tweet_terms);    
    for term in news_terms:             
        log_sum += log((tweet_terms.count(term) + miu * news_terms.count(term) / news_terms_total) /
                        (tweet_terms_total + miu))     
    score = log_sum
    return score

score.fields = ['terms']
