import requests
from boilerpipe.extract import Extractor
from six.moves.urllib.parse import urlsplit

from tweetRecommender.config import config
from tweetRecommender.mongo import mongo



def handle(uri):
    """News Article pipeline."""
    if exists(uri):
        return
    try:
        content = fetch(uri)
    except RuntimeError:
        return
    cleaned = boilerpipe(content)
    db.webpages.insert(dict(
        url = uri,
        content = cleaned,
    ))

def enqueue(uri):
    """Add a webpage to the pipeline."""
    if blacklisted(uri):
        return
    #XXX use message queue
    handle(uri)


def exists(uri):
    doc = mongo.db.webpages.find_one(dict(url = uri))
    return bool(doc)

def blacklisted(uri):
    domain = urlsplit(uri).hostname
    return domain in config['blacklist']

def fetch(uri):
    try:
        request = requests.get(uri)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(e)
    return request.text

def boilerpipe(html):
    EXTRACTOR="DefaultExtractor"
    extractor = Extractor(extractor=EXTRACTOR, html=html)
    return extractor.getText()
