from __future__ import division

import tweetRecommender.ldamodel as ldamodel
from tweetRecommender.tokenize import tokenize

from gensim import matutils   
import numpy as np

#http://stackoverflow.com/questions/22433884/python-gensim-how-to-calculate-document-similarity-using-the-lda-model
#similarity using hellinger distance better than cosine similarity for lda model    
def score(tweet, webpage):
    lda = ldamodel.get_lda()
    dictionary = ldamodel.get_dictionary()
    tweet_vec = lda[dictionary.doc2bow(tweet['terms'])]
    news_vec = lda[dictionary.doc2bow(tokenize(webpage["content"]))]
    dense1 = matutils.sparse2full(tweet_vec, lda.num_topics)
    dense2 = matutils.sparse2full(news_vec, lda.num_topics)
    sim = np.sqrt(0.5 * ((np.sqrt(dense1) - np.sqrt(dense2))**2).sum())
    print 1-sim
    return 1-sim 
