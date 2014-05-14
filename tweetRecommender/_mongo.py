from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId

class MongoConnector:
    ID = '_id'

    def __init__(self, host, database, username, password):
        self.client = client = MongoClient(host)
        self.db = db = client[database]
        db.authenticate(username, password)

    def by_id(self, collection, object_id):
        return self.db[collection].find_one({self.ID: ObjectId(object_id)})

    def coll(self, collection_or_name):
        if isinstance(collection_or_name, basestring):
            return self.db[collection_or_name]
        elif isinstance(collection_or_name, Collection):
            return collection_or_name
        else:
            raise TypeError(
                "must be either pymongo.Collection or collection name")
