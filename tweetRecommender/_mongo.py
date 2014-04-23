from bson.objectid import ObjectId
from motor import MotorClient
from motor import MotorCollection
from tornado import gen

class MongoConnector:
    def __init__(self, host, database, username, password):
        mongo_uri = "mongodb://%s:%s@%s:27017/%s" % (username, password, host, database)
        self.client = client = MotorClient(mongo_uri)
        self.db = db = client[database]

    def by_id(self, collection, object_id, callback = None):
        return self.db[collection].find_one({'_id': ObjectId(object_id)}, callback = callback)

    def coll(self, collection_or_name):
        if isinstance(collection_or_name, basestring):
            return self.db[collection_or_name]
        elif isinstance(collection_or_name, MotorCollection):
            return collection_or_name
        else:
            raise TypeError(
                "must be either pymongo.Collection or collection name")
