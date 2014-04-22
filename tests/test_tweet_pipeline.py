from .util import patch, mock_mongo; mock_mongo()
from tweetRecommender import resolution
from tweetRecommender.mongo import mongo

RESOLVED = "http://resolved/"
def _dummy_resolve(uri):
    return RESOLVED

@patch('tweetRecommender.resolution.resolve', _dummy_resolve)
def test_uri_matching():
    URL = "http://uri1/"
    TWEET = '123456abcdef'

    resolution.handle(URL, TWEET)
    assert mongo.db.redirects.find_one({'from': URL, 'to': RESOLVED})
    assert mongo.db.webpages_tweets.find_one(dict(url=RESOLVED))
