from .util import mock_mongo; mock_mongo()
from tweetRecommender import web as webprocessor
from tweetRecommender.mongo import mongo


def test_exists():
    URL = "http://foo/"
    mongo.db.webpages.insert(dict(url=URL))
    assert webprocessor.exists(URL)

def test_not_exists():
    URL = "http://bar/"
    assert not webprocessor.exists(URL)
