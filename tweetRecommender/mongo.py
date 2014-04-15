from pymongo import MongoClient
from bson.objectid import ObjectId
from tweetRecommender.config import config

class MongoConnector:
    def __init__(self, cfg=None):
        if cfg is None:
            cfg = config['mongodb']
        self.client = client = MongoClient(cfg['host'])
        self.db = db = client[cfg['database']]
        db.authenticate(cfg['user'], cfg['password'])

    def by_id(self, collection, object_id):
        return self.db[collection].find_one({'_id': ObjectId(object_id)})

mongo = MongoConnector()
