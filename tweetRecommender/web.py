import requests
from boilerpipe.extract import Extractor
from six.moves.urllib.parse import urlsplit

from tweetRecommender.config import config
from tweetRecommender.mongo import mongo
from tweetRecommender.tokenize import tokenize  

def tokenize_webpages(collection_ref):
    import sys

    coll = mongo.coll(collection_ref)

    count = 0
    docs = coll.find({'terms': {'$exists': False}})
    for doc in docs:
        sys.stdout.write("\r" + str(count))
        sys.stdout.flush()
        count += 1
        terms = tokenize(doc["content"].encode("utf-8"))
        coll.update({'url': doc["url"]}, {'$set': {'terms': terms}})


def handle(uri):
    """News Article pipeline."""
    if exists(uri):
        return
    try:
        content = fetch(uri)
    except RuntimeError:
        return
    cleaned = boilerpipe(content)
    terms = tokenize(cleaned)
    mongo.db.webpages.insert(dict(
        url = uri,
        content = cleaned,
        terms = terms
    ))

def enqueue(uri):
    """Add a webpage to the pipeline."""
    if blacklisted(uri):
        return
    #XXX use message queue
    handle(uri)


def exists(uri):
    doc = mongo.db.webpages.find_one(dict(url = uri), {'url'})
    return bool(doc)

def blacklisted(uri):
    if "://" not in uri:
        uri = "http://" + uri
    domain = urlsplit(uri).hostname
    return any(domain.split('.', nsuffix)[-1] in config['blacklist']
               for nsuffix in range(domain.count('.')+1))

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

if __name__ == '__main__':
    tokenize_webpages("sample_webpages_test")
