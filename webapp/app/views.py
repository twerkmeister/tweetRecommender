import random

from tweetRecommender.query import run as recommend, get_webpage
from tweetRecommender.mongo import mongo
from tweetRecommender import machinery

from app import app

from flask import request, session
from flask import render_template, redirect, send_file
from flask import url_for, jsonify


WEBPAGES_COLLECTION = 'sample_webpages'
TWEETS_COLLECTION = 'sample_tweets'
LIMIT = 10


def random_url():
    return mongo.random(WEBPAGES_COLLECTION)['url']

def random_options():
    gather = random.choice(list(machinery.find_components(
        machinery.GATHER_PACKAGE)))
    rankers = random.choice(list(machinery.find_components(
        machinery.SCORE_PACKAGE)))
    filters = random.choice(list(machinery.find_components(
        machinery.FILTER_PACKAGE)))

    return dict(
        gatheringMethod = gather,
        filteringMethods = filters,
        rankingMethods = rankers,
    )


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
            tweet["_id"] = str(tweet["_id"])

    except Exception, e:
        import traceback; traceback.print_exc()
    finally:
        return jsonify(result)

@app.route("/options")
def options():
    scoringMethods = list(machinery.find_components(machinery.SCORE_PACKAGE))
    gatheringMethods = list(machinery.find_components(machinery.GATHER_PACKAGE))
    filteringMethods = list(machinery.find_components(machinery.FILTER_PACKAGE))
    options = {"rankingMethods": scoringMethods,
    "gatheringMethods": gatheringMethods,
    "filteringMethods": filteringMethods}
    return jsonify(options)


@app.route("/evaluate", methods=['POST'])
def evaluate():
    uid = session.get('uid', '')
    options = request.json['options']
    webpage = request.json['webpage']
    rating = request.json['rating']

    mongo.db.evaluation.update(
        dict(uid=uid, options=options, webpage=webpage),
        {'$set': {'rankings.' + uid: rating}},
        dict(upsert=True),
    )

@app.route("/evaluation")
def evaluation():
    if not 'uid' in session:
        session['uid'] = uuid.uuid4().replace('-', '')
    webpage = random_url()
    options = random_options()
    return send_file('templates/evaluate.html')
