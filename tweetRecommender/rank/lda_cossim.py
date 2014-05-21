from __future__ import division

import tweetRecommender.ldamodel as ldamodel
from tweetRecommender.tokenize import tokenize  
import functools32

from gensim import matutils

#http://stackoverflow.com/questions/22433884/python-gensim-how-to-calculate-document-similarity-using-the-lda-model   
def score(tweet, webpage):        
    lda = ldamodel.get_lda()    
    dictionary = ldamodel.get_dictionary()    
    tweet_vec = lda[dictionary.doc2bow(tweet['terms'])]  
    news_vec = cached_news_vector(webpage["content"].encode("utf-8"))
    score = matutils.cossim(news_vec, tweet_vec)                
    return score

@functools32.lru_cache() 
def cached_news_vector(text):      
    return ldamodel.get_lda()[ldamodel.get_dictionary().doc2bow(tokenize(text))]  

FIELDS = ['terms']
