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

def get_features(tweet, webpage):
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
    return [None, lda_scores, lm_scores, tweet_length, chars, isverified,
                followers_count, statuses_count, listed_count, friends_count, 
                absolute_time_difference, relative_time_difference, binary_decision,
                capped_time_after, contains_url, url_count, hashtag_count]
    

def score(tweet, webpage):            
    return WekaClassifier.classify(get_features(tweet, webpage))       

score.fields = ['terms', 'user.verified', 'user.followers_count', 'user.statuses_count',
                'user.listed_count', 'user.friends_count', 'created_at', 'hashtags', 'full_urls']

#!/usr/bin/env python
""" generated source for module test_new """
class WekaClassifier(object):
    """ generated source for class WekaClassifier """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        sums = [0,0]
        sums[int(WekaClassifier_0.classify(i))] += 1.2134644010075073
        sums[int(WekaClassifier_1.classify(i))] += 0.57177685574344
        sums[int(WekaClassifier_2.classify(i))] += 0.40154496884580815
        sums[int(WekaClassifier_3.classify(i))] += 0.35999934750119333
        sums[int(WekaClassifier_4.classify(i))] += 0.36937329276984643
        sums[int(WekaClassifier_5.classify(i))] += 0.16351990613377496
        sums[int(WekaClassifier_6.classify(i))] += 0.1396078832952814
        sums[int(WekaClassifier_7.classify(i))] += 0.15882943193304253
        sums[int(WekaClassifier_8.classify(i))] += 0.1284505298097081
        sums[int(WekaClassifier_9.classify(i))] += 0.09903161346969916
        sums[int(WekaClassifier_10.classify(i))] += 0.19672733155497407
        sums[int(WekaClassifier_11.classify(i))] += 0.17672847093616786
        sums[int(WekaClassifier_12.classify(i))] += 0.18729151620386228
        sums[int(WekaClassifier_13.classify(i))] += 0.24810462685136855
        sums[int(WekaClassifier_14.classify(i))] += 0.23706555932983922
        sums[int(WekaClassifier_15.classify(i))] += 0.14276017880034322
        sums[int(WekaClassifier_16.classify(i))] += 0.2655207144416779
        sums[int(WekaClassifier_17.classify(i))] += 0.24759035974335297
        sums[int(WekaClassifier_18.classify(i))] += 0.14255881855351965
        sums[int(WekaClassifier_19.classify(i))] += 0.1181101393342422        
        return float(sums[0] - sums[1])


class WekaClassifier_0(object):
    """ generated source for class WekaClassifier_0 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 1
        elif (float(i[1])) <= 0.610257172808176:
            return 1
        else:
            return 0


class WekaClassifier_1(object):
    """ generated source for class WekaClassifier_1 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 1
        elif (float(i[1])) <= 0.1142382568740966:
            return 1
        else:
            return 1


class WekaClassifier_2(object):
    """ generated source for class WekaClassifier_2 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 0
        elif (float(i[1])) <= 0.1142382568740966:
            return 1
        else:
            return 0


class WekaClassifier_3(object):
    """ generated source for class WekaClassifier_3 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  relative_time_difference 
        if i[11] == None:
            return 1
        elif (float(i[11])) <= -4.831985E8:
            return 1
        else:
            return 0


class WekaClassifier_4(object):
    """ generated source for class WekaClassifier_4 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  tweet_length 
        if i[3] == None:
            return 1
        elif (float(i[3])) <= 14.5:
            return 1
        else:
            return 1


class WekaClassifier_5(object):
    """ generated source for class WekaClassifier_5 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  tweet_length 
        if i[3] == None:
            return 0
        elif (float(i[3])) <= 14.5:
            return 0
        else:
            return 1


class WekaClassifier_6(object):
    """ generated source for class WekaClassifier_6 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 1
        elif (float(i[1])) <= 0.02728102940334218:
            return 1
        else:
            return 1


class WekaClassifier_7(object):
    """ generated source for class WekaClassifier_7 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 0
        elif (float(i[1])) <= 0.02728102940334218:
            return 1
        else:
            return 0


class WekaClassifier_8(object):
    """ generated source for class WekaClassifier_8 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  chars 
        if i[4] == None:
            return 1
        elif (float(i[4])) <= 141.5:
            return 1
        else:
            return 1


class WekaClassifier_9(object):
    """ generated source for class WekaClassifier_9 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  chars 
        if i[4] == None:
            return 0
        elif (float(i[4])) <= 141.5:
            return 0
        else:
            return 1


class WekaClassifier_10(object):
    """ generated source for class WekaClassifier_10 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  friends_count 
        if i[9] == None:
            return 1
        elif (float(i[9])) <= 101.0:
            return 1
        else:
            return 0


class WekaClassifier_11(object):
    """ generated source for class WekaClassifier_11 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  statuses_count 
        if i[7] == None:
            return 1
        elif (float(i[7])) <= 85216.0:
            return 1
        else:
            return 1


class WekaClassifier_12(object):
    """ generated source for class WekaClassifier_12 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  statuses_count 
        if i[7] == None:
            return 0
        elif (float(i[7])) <= 85216.0:
            return 0
        else:
            return 1


class WekaClassifier_13(object):
    """ generated source for class WekaClassifier_13 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  chars 
        if i[4] == None:
            return 1
        elif (float(i[4])) <= 133.5:
            return 0
        else:
            return 1


class WekaClassifier_14(object):
    """ generated source for class WekaClassifier_14 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  language_model 
        if i[2] == None:
            return 1
        elif (float(i[2])) <= -7.848941176618522:
            return 0
        else:
            return 1


class WekaClassifier_15(object):
    """ generated source for class WekaClassifier_15 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  language_model 
        if i[2] == None:
            return 1
        elif (float(i[2])) <= -8.357419966171143:
            return 1
        else:
            return 0


class WekaClassifier_16(object):
    """ generated source for class WekaClassifier_16 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 1
        elif (float(i[1])) <= 0.891599215656381:
            return 1
        else:
            return 0


class WekaClassifier_17(object):
    """ generated source for class WekaClassifier_17 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 1
        elif (float(i[1])) <= 0.6215704159296479:
            return 0
        else:
            return 1


class WekaClassifier_18(object):
    """ generated source for class WekaClassifier_18 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  lda 
        if i[1] == None:
            return 1
        elif (float(i[1])) <= 0.01755814193254369:
            return 1
        else:
            return 0


class WekaClassifier_19(object):
    """ generated source for class WekaClassifier_19 """
    @classmethod
    def classify(cls, i):
        """ generated source for method classify """
        #  absolute_time_difference 
        if i[10] == None:
            return 1
        elif (float(i[10])) <= 3.546747E9:
            return 1
        else:
            return 1

