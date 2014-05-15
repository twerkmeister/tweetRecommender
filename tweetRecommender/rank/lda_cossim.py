from __future__ import division

import tweetRecommender.ldamodel as ldamodel
from tweetRecommender.config import config
from tweetRecommender.tokenize import tokenize  

from gensim import models, matutils
import functools32

@functools32.lru_cache() 
def get_lda():
    return models.LdaModel.load('c://tmp//news_lda_model.model')
    
@functools32.lru_cache() 
def get_dictionary():    
    return ldamodel.create_dictionary(config["lda"]["dict_path"])

#http://stackoverflow.com/questions/22433884/python-gensim-how-to-calculate-document-similarity-using-the-lda-model   
def score(tweet, webpage):        
    lda = get_lda()    
    dictionary = get_dictionary()    
    tweet_vec = lda[dictionary.doc2bow(tweet['terms'])]    
    news_vec = lda[dictionary.doc2bow(tokenize(webpage["content"]))]    
    score = matutils.cossim(news_vec, tweet_vec)                    
    return score
