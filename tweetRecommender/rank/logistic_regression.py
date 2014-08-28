from __future__ import division
from tweetRecommender import machinery
from tweetRecommender import log
from numpy import e

components = [("lda_cossim", 0.0707),("language_model",0.0819)]
intercept = 0.659
DISPLAY_NAME = "Logistic Regression"

#logistic regression weighting
#lda_cossim                                     -0.0707
#language_model                                 -0.0819
#text_overlap_plus_normalized_follower_count     0.0269
#Intercept                                        0.659
def score(tweet, webpage):
    score_funcs = [
            (machinery.load_component(
                machinery.SCORE_PACKAGE, ranker, machinery.SCORE_METHOD), weight)
            for ranker, weight in components]
    score = intercept
    for score_func, weight in score_funcs:    
            score += score_func(tweet, webpage) * weight            
    return sigmoid(score)        

def sigmoid(X):            
    den = 1.0 + e ** (-1.0 * X)
    d = 1.0 / den        
    return d

score.fields = ['terms']        