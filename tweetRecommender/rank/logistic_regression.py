from __future__ import division
from tweetRecommender import machinery
from tweetRecommender import log
from tweetRecommender.rank.adaboost import get_features
from numpy import e


components = [ 
 ("lda",1, 3.4911),
 ("language_model",2,0.1419),
 ("tweet_length",3,0.023),
 ("chars",4,-0.0091),
 ("isverified",5,-0.4062),
 ("followers_count",6,0),
 ("statuses_count",7,0),
 ("listed_count",8,0.0007),
 ("friends_count",9,0),
 ("absolute_time_difference",10, 0),
 ("relative_time_difference",11,0),
 ("binary_decision",12, -0.6374),
 ("capped_time_after",13,0),
 ("contains_url",14,  0.2031),
 ("url_count",15,0.2583),
 ("hashtag_count",16,0.0159)]
DISPLAY_NAME = "Logistic Regression"
intercept = -0.0154

def score(tweet, webpage):
    features = get_features(tweet, webpage)
    score = intercept
    for component in components:
        score += features[component[1]] * component[2]             
    return sigmoid(score)        

def sigmoid(X):            
    den = 1.0 + e ** (-1.0 * X)
    d = 1.0 / den        
    return d

score.fields = ['terms', 'user.verified', 'user.followers_count', 'user.statuses_count',
                'user.listed_count', 'user.friends_count', 'created_at', 'hashtags', 'full_urls'] 