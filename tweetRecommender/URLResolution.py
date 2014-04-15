'''
Created on Apr 14, 2014

@author: easten
'''

import urllib.request
from tweetRecommender.mongoconnector import mongo
from bson.objectid import ObjectId


def redirectExists(url):
    data = mongo.db.redirects.find_one({"from" : url})
    return bool(data)

def getRedirects(url):
    data = mongo.db.redirects.find_one({"from" : url})
    return data

def webpagesTweetsExist(url):
    cursor = mongo.db.webpages_tweets.find_one({"url" : url})
    return bool(cursor)

"""URL Resolution method get from tweets in MongoDB"""
def URLResolutionMongoDB(objectId):
    data = mongo.db.tweets.find_one({"_id" : objectId})
    url = data["urls"][0]
    urlData = getRedirects(url)

    """ check if url exist in redirects collection """
    if not (bool(urlData)):
        """ GET redirect url """
        response = urllib.request.urlopen(url)
        urlLink = response.geturl()
        mongo.db.redirects.insert({"from" : url, "url" : urlLink})
    else:
        urlLink = urlData["to"]

    """" check whether tweets exist inside the webpages_tweets table"""
    webpage = mongo.db.webpages_tweets.find_one({"url" : urlLink})
    if (bool(webpage)):
        """ use addToSet so there is no duplication in the array """
        mongo.db.webpages_tweets.update({"url" : urlLink}, {"$addToSet" : {"tweets" : objectId}})
    else:
        mongo.db.webpages_tweets.insert({"url" : urlLink,  "tweets" : [objectId]})

    print("tweets resolution done")

if __name__ == '__main__':
    URLResolutionMongoDB(ObjectId("52adb77a00323226c3b871dc"))

