from mongoconnector import MongoConnector

db = MongoConnector().db

print(db.collection_names())