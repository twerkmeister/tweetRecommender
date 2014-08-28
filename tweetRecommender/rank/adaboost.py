from __future__ import division
from tweetRecommender import machinery
from tweetRecommender import log
import datetime
import math

DISPLAY_NAME = "AdaBoost DecisionStump"
LOG = log.getLogger('tweetRecommender.query')
epoch = datetime.datetime(1970, 1, 1)

def get_absolute_time(webpage_creation_time, tweet_creation_time):
    return math.fabs(float(webpage_creation_time- tweet_creation_time))

def get_relative_time(webpage_creation_time, tweet_creation_time):
    return tweet_creation_time - webpage_creation_time

#webpage published... (-1: before, 1: after)
def get_binary_time_decision(webpage_creation_time, tweet_creation_time):    
    if (tweet_creation_time - webpage_creation_time) >= 0:
        return 1
    return -1

# return 0 for all tweets published before webpage and real value for other
def get_capped_time(webpage_creation_time, tweet_creation_time):
    if (tweet_creation_time - webpage_creation_time) > 0:
        return tweet_creation_time - webpage_creation_time
    return 0

def score(tweet, webpage):    
    tweet_length = len(tweet["terms"])     #number of terms after stopword removal and stemming
    chars = len(tweet["text"])
    isverified = tweet["user"]["verified"]
    followers_count = tweet["user"]["followers_count"]
    statuses_count = tweet["user"]["statuses_count"]
    listed_count = tweet["user"]["listed_count"]
    friends_count = tweet["user"]["friends_count"]    
    webpage_creation_time = (epoch - webpage['created_at']).total_seconds() * 1000
    tweet_creation_time = (epoch - tweet["created_at"]).total_seconds() * 1000
    absolute_time_difference = get_absolute_time(webpage_creation_time, tweet_creation_time)
    relative_time_difference = get_relative_time(webpage_creation_time, tweet_creation_time)
    binary_decision = get_binary_time_decision(webpage_creation_time, tweet_creation_time) 
    capped_time_after = get_capped_time(webpage_creation_time, tweet_creation_time)
    contains_url = False 
    if tweet["full_urls"] == webpage["url"]:
        contains_url  = True        
    contains_url = contains_url
    url_count = len(tweet["full_urls"])
    hashtag_count = len(tweet["hashtags"])
    lda_scores = machinery.load_component(machinery.SCORE_PACKAGE, "lda_cossim", machinery.SCORE_METHOD)(tweet, webpage)
    lm_scores = machinery.load_component(machinery.SCORE_PACKAGE, "language_model", machinery.SCORE_METHOD)(tweet, webpage)
    #the first element is rank in weka, set to none)        
    features = [None, lda_scores, lm_scores, tweet_length, chars, isverified,
                followers_count, statuses_count, listed_count, friends_count, 
                absolute_time_difference, relative_time_difference, binary_decision,
                capped_time_after, contains_url, url_count, hashtag_count]
    #LOG.info("features are : ")
    #LOG.info(features)
    return WekaClassifier.classify(features)       

score.fields = ['terms', 'user.verified', 'user.followers_count', 'user.statuses_count',
                'user.listed_count', 'user.friends_count', 'created_at', 'hashtags', 'full_urls']

class WekaClassifier(object):
    """ generated source for class WekaClassifier """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        sums = [0,0]
        sums[int(WekaClassifier_0.classify(i))] += 1.0370543956686762
        sums[int(WekaClassifier_1.classify(i))] += 0.42646991959300357
        sums[int(WekaClassifier_2.classify(i))] += 0.6130850163011905
        sums[int(WekaClassifier_3.classify(i))] += 0.35939569291671875
        sums[int(WekaClassifier_4.classify(i))] += 0.3008681122335692
        sums[int(WekaClassifier_5.classify(i))] += 0.3040994319524441
        sums[int(WekaClassifier_6.classify(i))] += 0.14540078862818462
        sums[int(WekaClassifier_7.classify(i))] += 0.3249327557181082
        sums[int(WekaClassifier_8.classify(i))] += 0.05379180819513292
        sums[int(WekaClassifier_9.classify(i))] += 0.06882327060765335        
        return float(sums[0]-sums[1])


class WekaClassifier_0(object):
    """ generated source for class WekaClassifier_0 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[1] == None:
            return 0
        elif (float(i[1])) <= 0.7680270780214076:
            return 1
        else:
            return 0


class WekaClassifier_1(object):
    """ generated source for class WekaClassifier_1 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[1] == None:
            return 1
        elif (float(i[1])) <= 0.8924443408713842:
            return 1
        else:
            return 0


class WekaClassifier_2(object):
    """ generated source for class WekaClassifier_2 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[10] == None:
            return 1
        elif (float(i[10])) <= 4.147055E8:
            return 0
        else:
            return 1


class WekaClassifier_3(object):
    """ generated source for class WekaClassifier_3 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[10] == None:
            return 1
        elif (float(i[10])) <= 4.6651785E9:
            return 1
        else:
            return 0


class WekaClassifier_4(object):
    """ generated source for class WekaClassifier_4 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[8] == None:
            return 0
        elif (float(i[8])) <= 2.5:
            return 0
        else:
            return 1


class WekaClassifier_5(object):
    """ generated source for class WekaClassifier_5 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[2] == None:
            return 0
        elif (float(i[2])) <= -8.577972043571158:
            return 1
        else:
            return 0


class WekaClassifier_6(object):
    """ generated source for class WekaClassifier_6 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[11] == None:
            return 1
        elif (float(i[11])) <= -4.5163605E9:
            return 0
        else:
            return 1


class WekaClassifier_7(object):
    """ generated source for class WekaClassifier_7 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[9] == None:
            return 0
        elif (float(i[9])) <= 208.5:
            return 1
        else:
            return 0


class WekaClassifier_8(object):
    """ generated source for class WekaClassifier_8 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[11] == None:
            return 0
        elif (float(i[11])) <= -4.5163605E9:
            return 0
        else:
            return 0


class WekaClassifier_9(object):
    """ generated source for class WekaClassifier_9 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        if i[11] == None:
            return 0
        elif (float(i[11])) <= -4.5163605E9:
            return 0
        else:
            return 1


        