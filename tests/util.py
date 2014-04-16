from mock import patch
import mongomock

from tweetRecommender._mongo import MongoConnector

class MockMongoConnector(MongoConnector):
    client = mongomock.Connection()
    db = client.db
    def __init__(self, **kwargs):
        pass

def mock_mongo():
    patcher = patch('tweetRecommender._mongo.MongoConnector', MockMongoConnector)
    patcher.start()
