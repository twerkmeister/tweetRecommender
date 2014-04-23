'''
Created on Apr 14, 2014

@author: easten
'''
from bson.objectid import ObjectId
import requests

from tweetRecommender.mongo import mongo


def find_redirect(url):
    data = mongo.db.redirects.find_one({"from" : url})
    if data:
        return data["to"]

def resolve(url):
    try:
        response = requests.head(url)
    except requests.exceptions.RequestException:
        return url
    return response.headers.get('Location', url)


def handle(url, tweet_id):
    redirect = find_redirect(url)
    if not redirect:
        redirect = resolve(url)
        mongo.db.redirects.insert({'from': url, 'to': redirect.encode('utf-8')})

    mongo.db.tweets.update({'_id': tweet_id},
                           {'$addToSet': {'full_urls': redirect}})
    return redirect

def handle_mongo(tweet_id):
    doc = mongo.by_id('tweets', tweet_id)
    for url in doc["urls"]:
        handle(url, tweet_id)

def handle_tweet(tweet):
    for url in tweet["urls"]:
        handle(url, tweet['_id'])


if __name__ == '__main__':
    handle_mongo("52adb77a00323226c3b871dc")
