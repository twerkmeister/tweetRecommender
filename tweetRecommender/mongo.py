from pymongo import MongoClient
from pymongo.collection import Collection
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

    def coll(self, collection_or_name):
        if isinstance(collection_or_name, basestring):
            return self.db[collection_or_name]
        elif isinstance(collection_or_name, Collection):
            return collection_or_name
        else:
            raise TypeError(
                "must be either pymongo.Collection or collection name")

mongo = MongoConnector()
