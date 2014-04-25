from .util import mock_mongo, patch; mock_mongo()
from tweetRecommender import web as webprocessor
from tweetRecommender.mongo import mongo


def test_exists():
    URL = "http://foo/"
    mongo.db.webpages.insert(dict(url=URL))
    assert webprocessor.exists(URL)

def test_not_exists():
    URL = "http://bar/"
    assert not webprocessor.exists(URL)

@patch('tweetRecommender.web.config', dict(blacklist=["example.com"]))
def test_blacklist():
    assert webprocessor.blacklisted("example.com")
    assert not webprocessor.blacklisted("example.net")

@patch('tweetRecommender.web.config', dict(blacklist=["example.com"]))
def test_blacklist_subdomain():
    assert webprocessor.blacklisted("www.example.com")
