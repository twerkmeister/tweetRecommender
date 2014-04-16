from tweetRecommender.config import config
from tweetRecommender._mongo import MongoConnector

cfg = config['mongodb']
mongo = MongoConnector(
    host = cfg['host'],
    database = cfg['database'],
    username = cfg['user'],
    password = cfg['password'],
)
