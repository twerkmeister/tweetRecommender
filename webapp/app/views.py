from tweetRecommender.query import run as recommend
from tweetRecommender.query import evaluation_run
from tweetRecommender.mongo import mongo
from tweetRecommender import machinery
from tweetRecommender.query import get_webpage
from tweetRecommender.query import get_webpage_for_id
from tweetRecommender import log

from app import app

from flask import request, session
from flask import render_template, redirect, send_file
from flask import url_for, jsonify

import uuid
from itertools import chain
import random
import os

log.basicConfig(
        level = log.DEBUG,
        format = "[%(levelname)s] %(message)s",
    )

URLS_FILE = os.path.join(os.path.dirname(__file__), "urls.txt")
URLS = file(URLS_FILE).read().split("\n")[:-1]

TWEETS_COLLECTION = 'sample_tweets'
WEBPAGES_COLLECTION = 'sample_webpages'
EVALUATION_COLLECTION = 'evaluation'
LIMIT = 10

def random_url():
    return mongo.random(WEBPAGES_COLLECTION)['url']

def random_evaluation_url(urls=URLS):
    return random.choice(URLS)

def next_evaluation_url(evaluated):
    urls = URLS[:]
    for url in evaluated:
        try:
            urls.remove(url)
        except:
            log.debug("ERROR WHILE REMOVING")
            pass #url is not in the pool anymore
    log.debug("URLS NOT EVALUATED: %s" % str(len(urls)))
    next_url = random_evaluation_url(urls)
    log.debug("Next url: %s" % next_url)
    return next_url
    #return URLS[len(evaluated) % len(URLS)]

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

def run_evaluation_query(url):
    result = []
    try:
        result = evaluation_run(url)

        for score, tweet in result:
            tweet["_id"] = str(tweet["_id"])
            tweet["score"] = score

        #consolidate score and tweets
        result = [tweet for score, tweet in result]

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
    tweetId = request.json['tweetId']
    webpage = request.json['webpage']
    rating = request.json['rating']

    mongo.db.evaluation.insert(
        dict(tweet=tweetId, uid=uid, webpage=webpage, rating=rating)
    )
    return jsonify({"success": 1})

@app.route("/evaluation")
def evaluation():
    if not 'uid' in session:
        session['uid'] = str(uuid.uuid4()).replace('-', '')
    return send_file('static/html/evaluate.html')

@app.route("/evaluation/next")
def evaluation_next():
    url = next_evaluation_url(get_evaluated_articles())
    log.info("Current URL: %s" % url)
    webpage = get_webpage(url, mongo.coll(WEBPAGES_COLLECTION))
    tweets = run_evaluation_query(url)
    result = {"url": url, "tweets": tweets, "newsId": str(webpage["_id"])}
    return jsonify(result)


@app.route("/impressum")
def impressum():
    return send_file("static/html/impressum.html")

@app.route("/about")
def about():
    return send_file("static/html/about.html")

@app.route("/article/<webpage_id>", methods=['GET'])
def get_article(webpage_id):
    webpage = get_webpage_for_id(webpage_id, mongo.coll(WEBPAGES_COLLECTION))
    article = "No article found with id %s!" % webpage_id
    url = ""
    num_articles = len(set(get_evaluated_articles()).intersection(set(URLS)))
    if webpage:
        article = webpage.get("article", webpage["content"]).encode("utf-8")
        url = webpage["url"]
    return jsonify({"article": article, "_id": webpage_id, "url": url, 'num_articles' : str(num_articles)})

def get_evaluated_articles():
    uid = session.get('uid', '')    
    webpages = list(mongo.coll(EVALUATION_COLLECTION).find({'uid' : uid},{'webpage' : 1}).distinct('webpage'))
    log.debug("WEBPAGES EVALUATED BY USER %s:" % (uid))
    log.debug("%s" % (";".join(webpages)))
    return webpages
