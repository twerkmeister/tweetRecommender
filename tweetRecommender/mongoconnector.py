import os
from pymongo import MongoClient
from tweetRecommender.config import config

class MongoConnector:
    def __init__(self, cfg=None):
        if config is None:
            cfg = config['mongodb']
        self.client = client = MongoClient(cfg['host'])
        self.db = db = client[cfg['database']]
        db.authenticate(cfg['user'], cfg['password'])

mongo = MongoConnector()
