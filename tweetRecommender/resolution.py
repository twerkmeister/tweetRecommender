'''
Created on Apr 14, 2014

@author: easten
'''

import requests
from bson.objectid import ObjectId
from tweetRecommender.mongo import mongo


def find_redirect(url):
    data = mongo.db.redirects.find_one({"from" : url})
    if data:
        return data["to"]

def resolve(url):
    response = requests.head(url)
    redirect = response.headers['Location']
    return redirect or url


def handle(url):
    redirect = find_redirect(url)
    if not redirect:
        redirect = resolve(url)
        mongo.db.redirects.insert(dict(
            url = url,
            redirect = redirect,
        )

    mongo.db.webpages_tweets.update({"url": url},
                                    {"$addToSet": {"tweets": object_id}},
                                    {"upsert": True})

def handle_mongo(object_id):
    doc = mongo.by_id('tweets', object_id)
    for url in data["urls"]:
        handle(url)


if __name__ == '__main__':
    handle_mongo("52adb77a00323226c3b871dc")
