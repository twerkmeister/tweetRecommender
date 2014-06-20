import operator
from tweetRecommender import log

term_similarity = 1

def diversity(result, limit, tweets_index):
    log.debug("remove similar tweets..")            
    tweet_terms = dict();    
    for i,tweet in enumerate(result[:limit]):
        tweet_text = tweets_index[tweet[1]]["text"];
        hashtag_set = set([tag.strip("#") for tag in tweet_text.split() if tag.startswith("#")])        
        tweet_terms[i] = set(tweets_index[tweet[1]]["terms"]) - hashtag_set #remove hashtag terms 
    removes = []
    for key in tweet_terms:         
        for key_1 in tweet_terms:
            if key != key_1 and key not in removes:                
                if(len(tweet_terms[key].difference(tweet_terms[key_1])) <= term_similarity):                                    
                    removes.append(key_1)
                    break                
    if len(removes) == 0:        
        return result[:limit]
    else:
        offset = 0
        for index in sorted(removes, reverse=False):
            #print "remove: ", tweets_index[result[index-offset][1]]["text"].encode("utf-8")            
            del result[index-offset]
            offset += 1           
        diversity((result), limit, tweets_index)
                       
    return result[:limit]