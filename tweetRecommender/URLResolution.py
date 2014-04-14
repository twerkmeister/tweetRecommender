'''
Created on Apr 14, 2014

@author: easten
'''

import urllib.request
from mongoconnector import mongo
                                
    
def redirectExists(url):            
    cursor = mongo.db.redirects.find_one({"from" : url})                
    return bool(cursor)

def insertIndexes(url):
    "'not yet done'"
    if not (mongo.db.webpages_tweets.find_one({"url": url})):    
        mongo.db.webpages_tweets.insert("we")
    
def URLResolution(url):
    if not (redirectExists(url)):        
        response = urllib.request.urlopen(url)
        urlLink = response.geturl()
        mongo.db.redirects.insert({"from" : url, "url" : urlLink})                  
    else:            
        print("exist")    
        
if __name__ == '__main__':    
    URLResolution('http://spon.de/aecUM')    
    
    
    
    