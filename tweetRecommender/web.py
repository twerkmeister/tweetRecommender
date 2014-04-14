import requests
from boilerpipe.extract import Extractor

from tweetrecommender.config import config
from tweetrecommender.mongoconnector import mongo

try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit


def handle(uri):
    """News Article pipeline."""
    if exists(uri):
        return
    if blacklisted(uri):
        return
    content = fetch(uri)
    cleaned = boilerpipe(content)
    db.webpages.insert(dict(
        url = uri,
        content = cleaned,
    ))

def enqueue(uri):
    """Add a webpage to the pipeline."""
    #XXX use message queue
    handle(uri)


def exists(uri):
    doc = mongo.db.webpages.find_one(dict(url = uri))
    return bool(doc)

def blacklisted(uri):
    domain = urlsplit(uri).hostname
    return domain in config['blacklist']

def fetch(uri):
    request = requests.get(uri)
    return request.text

def boilerpipe(html):
    extractor = Extractor(extractor=EXTRACTOR, html=html)
    return extractor.getText()
