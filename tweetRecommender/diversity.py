from tweetRecommender import log
from tweetRecommender.tokenize import tokenize_diversity

term_similarity = 2

def diversity(result, limit, tweets_index):        
    log.debug("remove similar tweets..")                
    result_topK = [];        
    for tweet in result:
        similar = False                
        for tweet_1 in result_topK:
            if (len(get_clean_terms(tweets_index, tweet_1).symmetric_difference(get_clean_terms(tweets_index, tweet))) 
                <= term_similarity):
                similar = True                
        if (similar == False):
            result_topK.append(tweet)                
            if len(result_topK) >= limit:
                break;                     
    return result_topK

def get_clean_terms(tweets_index, tweet):
    return set(tokenize_diversity(tweets_index[tweet[1]]["text"]))  