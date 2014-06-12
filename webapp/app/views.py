from tweetRecommender.query import run as recommend
from tweetRecommender.mongo import mongo

from tweetRecommender.query import SCORE_PACKAGE, GATHER_PACKAGE, FILTER_PACKAGE
from tweetRecommender.machinery import load_component, find_components

from tweetRecommender.query import get_webpage

from app import app
from flask import render_template, request, url_for, redirect, jsonify, send_file, session


WEBPAGES_COLLECTION = 'sample_webpages'
TWEETS_COLLECTION = 'sample_tweets'
LIMIT = 10


def random_url():
    return mongo.random(WEBPAGES_COLL)['url']


@app.route("/", methods=['GET'])
def index():
    return send_file('templates/index.html')

@app.route("/url", methods=['GET'])
def url():
    return jsonify(dict(url=random_url()))


@app.route("/query", methods=['POST'])
def query():
    gatheringMethod = request.json["gatheringMethod"]
    filteringMethods = request.json["filteringMethods"]
    rankingMethods = request.json["rankingMethods"]
    action = request.json["action"]
    url = request.json["url"]

    result = {"tweets": []}
    try:
        result["tweets"] = recommend(url, gatheringMethod, rankingMethods, filteringMethods,
                           ['user.screen_name', 'created_at', 'text'],
                           TWEETS_COLLECTION, WEBPAGES_COLLECTION, LIMIT)

        for score, tweet in result["tweets"]:
            tweet.pop("_id")

    except Exception, e:
        import traceback; traceback.print_exc()
    finally:
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
