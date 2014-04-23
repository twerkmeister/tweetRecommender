from util import mock_mongo; mock_mongo()
from tweetRecommender import query
from tweetRecommender.mongo import mongo
from bson.objectid import ObjectId

tweets = [];

def insert_fake_data():
    fake_tweets = [{"text" : "tweet test 1", "user"  : {"followers_count" : 50,"friends_count" : 100}},
    {"text" : "tweet test 2", "user"  : {"followers_count" : 100,"friends_count" : 100}},
    {"text" : "tweet test 3", "user"  : {"followers_count" : 150,"friends_count" : 100}}]    
    for tweet in fake_tweets:       
        tweets.append(ObjectId(mongo.db.tweets.insert(tweet)));      
    fake_webpages_tweets = {"tweets" : tweets, "url" : "www.test.com"}
    mongo.db.webpages_tweets.insert(fake_webpages_tweets)
    
def test_gather():        
    insert_fake_data()       
    for data in query.gather("www.test.com"):        
        assert data["_id"] in tweets

def test_rank():        
    insert_fake_data()                            
    value = 0            
    for data in query.rank(query.gather("www.test.com")):                                          
        assert not value >= data[1]                                         
        
if __name__ == "__main__":
    test_gather()
    test_rank()
