from tweetRecommender.query import run as recommend
from tweetRecommender.mongo import mongo

from tweetRecommender.query import SCORE_PACKAGE, GATHER_PACKAGE, FILTER_PACKAGE
from tweetRecommender.machinery import load_component, find_components

from app import app
from flask import render_template, request, url_for, redirect, jsonify, send_file

from random import randint

@app.route("/", methods=['GET'])
def index():
    return send_file('templates/index.html')	

@app.route("/query", methods=['POST'])
def query():
    if request.method == 'POST':    
        limit = 10
        gatheringMethod = request.json["gatheringMethod"]
        filteringMethods = request.json["filteringMethods"]
        rankingMethods = request.json["rankingMethods"]
        action = request.json["action"]
        result = {"tweets": []}    
        try:
            if action == "search":
                url = request.form.get('url')
            elif action == "random":
                random_max = mongo.db["sample_webpages"].count() - 1
                random_webpage = mongo.db["sample_webpages"].find().skip(randint(0, random_max)).limit(1)[0]
                url = random_webpage.get('url')  
            else:
                 raise ValueError("invalid action")
            
            result["tweets"] = recommend(url, gatheringMethod, rankingMethods, filteringMethods, 
                               ['user.screen_name', 'created_at', 'text'], 
                               'sample_tweets', 'sample_webpages', limit)
            
            for score, tweet in result["tweets"]:
                tweet.pop("_id")

            return jsonify(result)

        except Exception, e:
            import traceback; traceback.print_exc()
            return jsonify(result)

@app.route("/options")
def options():
    scoringMethods = list(find_components(SCORE_PACKAGE))
    gatheringMethods = list(find_components(GATHER_PACKAGE))
    filteringMethods = list(find_components(FILTER_PACKAGE))
    options = {"rankingMethods": scoringMethods,
    "gatheringMethods": gatheringMethods,
    "filteringMethods": filteringMethods}
    return jsonify(options)
