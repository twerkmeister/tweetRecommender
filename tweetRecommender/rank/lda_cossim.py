from __future__ import division

import tweetRecommender.bow as bow
from gensim import models, matutils 

lda = models.LdaModel.load('tmp/news_lda_model.model')
dictionary = bow.create_dictionary("tmp/mongocorpus.dict")

#http://stackoverflow.com/questions/22433884/python-gensim-how-to-calculate-document-similarity-using-the-lda-model    
def score(tweet, tokenized_webpage):                            
    tweet_vec = lda[dictionary.doc2bow(tweet['terms'])]    
    news_vec = lda[dictionary.doc2bow(tokenized_webpage)]
    score = matutils.cossim(news_vec, tweet_vec)                   
    return score
