from tweetRecommender.config import config
import re

def check(tweet):
    return check_size(tweet.text) and check_author_credibility(tweet)

def check_size(text):
	cleaned = clean_tweet(text)
	return len(cleaned) >= config['tweet_min_length']

def clean_tweet(text):	     
    # thanks to http://ravikiranj.net/drupal/201205/code/machine-learning/how-build-twitter-sentiment-analyzer
    text = text.lower() #Convert to lower case    
    text = re.sub('((www\.[\s]+)|(https?://[^\s]+))','',text) #Convert www.* or https?://* to EMPTY STRING    
    text = re.sub('@[^\s]+','',text) #Convert @username to EMPTY STRING    
    text = re.sub('[\s]+', ' ', text) #Remove additional white spaces    
    text = re.sub(r'#([^\s]+)', r'\1', text) #Replace #word with word
    text = re.sub(r'\brt\b','', text) #Replace retweet with empty string    
    text = text.strip('\'"') #trim        
    return text

def check_author_credibility(user):
	if not user['verified']:
		return False
	if user['followers_count'] < config['followers_count']:
		return False

	#XXX useful?
	#if not whitelist(user['user_id']):
	#	return False
	#if blacklist(user['user_id']):
	#	return False

	return True
    
if __name__ == "__main__":        
    print clean_tweet("RT @RevolutionSyria: (08-15-13) #Daraa #Syria l Rebels Lay Siege to #Assad Hagana Battalion by border in Daraa http://t.co/RMfQhlU2Jr http://www.test.com")    
