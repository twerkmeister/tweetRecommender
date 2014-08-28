from tweetRecommender import log
from tweetRecommender.tokenize import tokenize_diversity

term_similarity = 1

def diversity(result, limit, tweets_index):        
    log.debug("remove similar tweets..")                
    result_topK = [];        
    for tweet in result:
        similar = False                
        for tweet_1 in result_topK:
            if (len(get_clean_terms(tweets_index[tweet_1[1]]["text"]).symmetric_difference(
                    get_clean_terms(tweets_index[tweet[1]]["text"]))) 
                    <= term_similarity):
                similar = True                
        if (similar == False):
            result_topK.append(tweet)                
            if len(result_topK) >= limit:
                break;                     
    return result_topK

def get_clean_terms(tweet):
    return set(tokenize_diversity(tweet))  

def new_tweet_is_different(tweet_list, new_tweet):
    if len(tweet_list) == 0:
        return True
    for score, tweet in tweet_list:
        if (len(get_clean_terms(new_tweet[1]["text"]).symmetric_difference(get_clean_terms(tweet["text"]))) 
                <= term_similarity):
            return False 
    return True
