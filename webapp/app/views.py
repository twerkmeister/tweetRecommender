import random

from tweetRecommender.query import run as recommend
from tweetRecommender.mongo import mongo
from tweetRecommender import machinery
from tweetRecommender.query import get_webpage

from app import app

from flask import request, session
from flask import render_template, redirect, send_file
from flask import url_for, jsonify

import uuid
from itertools import chain
from random import shuffle


TWEETS_COLLECTION = 'sample_tweets'
WEBPAGES_COLLECTION = 'sample_webpages'
LIMIT = 10

EVALUATION_GATHERING = "terms"
EVALUATION_FILTERING = []
EVALUATION_RANKING = [["language_model"], ["lda_cossim"], ["text_overlap", "date", "follower_count"]]

class MethodSet:
    def __init__(self, gatherer, filters, rankers):
        self.gatherer = gatherer
        self.filters = filters
        self.rankers = rankers

EVALUATION_CANDIDATES = [
    MethodSet("terms", ["expected_time"], ["language_model"]),
    MethodSet("terms", ["expected_time"], ["lda_cossim"]),
    MethodSet("terms", ["expected_time"], ["text_overlap", "date", "follower_count"])
]

def random_url():
    return mongo.random(WEBPAGES_COLLECTION)['url']

def random_options():
    gather = random.choice(list(machinery.find_components(
        machinery.GATHER_PACKAGE)))
    rankers = [random.choice(list(machinery.find_components(
        machinery.SCORE_PACKAGE)))]
    filters = [random.choice(list(machinery.find_components(
        machinery.FILTER_PACKAGE)))]

    return dict(
        gatheringMethod = gather,
        filteringMethods = filters,
        rankingMethods = rankers,
    )

@app.route("/", methods=['GET'])
def index():
    return send_file('static/html/index.html')

@app.route("/url", methods=['GET'])
def url():
    return jsonify(dict(url=random_url()))


@app.route("/query", methods=['POST'])
def query():
    gatheringMethod = request.json["gatheringMethod"]
    filteringMethods = request.json["filteringMethods"]
    rankingMethods = request.json["rankingMethods"]
    url = request.json["url"]

    return jsonify(run_query(url, gatheringMethod, rankingMethods, filteringMethods))

def run_query(url, gatheringMethod, rankingMethods, filteringMethods, limit = LIMIT):
    result = {"webpage": "", "tweets": []}
    try:
        result["webpage"] = get_webpage(url, mongo.coll(WEBPAGES_COLLECTION))["url"].encode('utf-8')
        result["tweets"] = recommend(url, gatheringMethod, rankingMethods, filteringMethods,
                           ['user.screen_name', 'created_at', 'text'],
                           TWEETS_COLLECTION, WEBPAGES_COLLECTION, limit)

        for score, tweet in result["tweets"]:
            tweet["_id"] = str(tweet["_id"])
            tweet["score"] = score
            tweet["options"] = {}
            tweet["options"]["gatheringMethod"] = gatheringMethod
            tweet["options"]["filteringMethods"] = filteringMethods
            tweet["options"]["rankingMethods"] = rankingMethods

        #consolidate score and tweets
        result["tweets"] = [tweet for score, tweet in result["tweets"]]

    except Exception, e:
        import traceback; traceback.print_exc()
    finally:
        return result

@app.route("/options")
def options():
    def get_modules_with_display_name(package):
        modules = list(machinery.find_components(package))
        return [(module, machinery.get_display_name(package, module)) for module in modules]
    scoringMethods = get_modules_with_display_name(machinery.SCORE_PACKAGE)
    gatheringMethods = get_modules_with_display_name(machinery.GATHER_PACKAGE)
    filteringMethods = get_modules_with_display_name(machinery.FILTER_PACKAGE)
    options = {"rankingMethods": scoringMethods,
    "gatheringMethods": gatheringMethods,
    "filteringMethods": filteringMethods}
    return jsonify(options)


@app.route("/evaluate", methods=['POST'])
def evaluate():
    uid = session.get('uid', '')
    tweet = request.json['tweetId']
    options = request.json['options']
    webpage = request.json['webpage']
    rating = request.json['rating']

    mongo.db.evaluation.update(
        dict(tweet=tweet, uid=uid, options=options, webpage=webpage),
        {'$set': {'rankings.' + uid: rating}},
        upsert=True
    )
    return jsonify({"success": 1})

@app.route("/evaluation")
def evaluation():
    if not 'uid' in session:
        session['uid'] = str(uuid.uuid4()).replace('-', '')
    return send_file('static/html/evaluate.html')

@app.route("/evaluation/next")
def evaluation_next():
    url = random_url()
    tweets_combined = [run_query(url, ms.gatherer, ms.rankers, ms.filters)["tweets"] for ms in EVALUATION_CANDIDATES]
    tweets = list(chain.from_iterable(tweets_combined))
    shuffle(tweets)
    result = {"url": url, "tweets": tweets}
    return jsonify(result)


@app.route("/impressum")
def impressum():
    return send_file("static/html/impressum.html")

@app.route("/article", methods=['POST'])
def get_article():
    article = ""    
    try:        
        url = request.json["url"]                                
        object = get_webpage(url, mongo.coll(WEBPAGES_COLLECTION))        
        if "article" in object:
            article = object["article"].encode("utf-8")
        else:
            article = object["content"].encode("utf-8")                                    
    except Exception, e:
        import traceback; traceback.print_exc()
    finally:
        return jsonify({"article" : article, "url" : url})
