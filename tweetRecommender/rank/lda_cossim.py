from __future__ import division

import tweetRecommender.ldamodel as ldamodel
from tweetRecommender.tokenize import tokenize  

from gensim import matutils

#http://stackoverflow.com/questions/22433884/python-gensim-how-to-calculate-document-similarity-using-the-lda-model   
def score(tweet, webpage):        
    lda = ldamodel.get_lda()    
    dictionary = ldamodel.get_dictionary()    
    tweet_vec = lda[dictionary.doc2bow(tweet['terms'])]  
    news_vec = lda[dictionary.doc2bow(tokenize(webpage["content"]))]    
    score = matutils.cossim(news_vec, tweet_vec)                
    return score
