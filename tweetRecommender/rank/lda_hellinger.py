from __future__ import division

import tweetRecommender.ldamodel as ldamodel
from tweetRecommender.config import config
from tweetRecommender.tokenize import tokenize

from gensim import models, matutils   
import numpy as np
import functools32

@functools32.lru_cache() 
def get_lda():
    return models.LdaModel.load('c://tmp//news_lda_model.model')
    
@functools32.lru_cache() 
def get_dictionary():    
    return ldamodel.create_dictionary(config["lda"]["dict_path"])

#http://stackoverflow.com/questions/22433884/python-gensim-how-to-calculate-document-similarity-using-the-lda-model
#similarity using hellinger distance better than cosine similarity for lda model    
def score(tweet, webpage):
    lda = get_lda()    
    dictionary = get_dictionary()
    tweet_vec = lda[dictionary.doc2bow(tweet['terms'])]
    news_vec = lda[dictionary.doc2bow(tokenize(webpage["content"]))]
    dense1 = matutils.sparse2full(tweet_vec, lda.num_topics)
    dense2 = matutils.sparse2full(news_vec, lda.num_topics)
    sim = np.sqrt(0.5 * ((np.sqrt(dense1) - np.sqrt(dense2))**2).sum())
    return 1-sim 
