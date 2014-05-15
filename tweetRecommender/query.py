#!/usr/bin/env python

from __future__ import print_function
import argparse
from importlib import import_module
from inspect import getargspec
import operator
import Queue

from tweetRecommender.mongo import mongo
from tweetRecommender.util import call_asmuch, set_vars
from tweetRecommender.evaluation import evaluate_query


#XXX maybe use config values?
GATHER_PACKAGE = 'tweetRecommender.gather'
GATHER_MODULE = 'terms'
GATHER_METHOD = 'gather'
SCORE_PACKAGE = 'tweetRecommender.rank'
SCORE_MODULE = 'text_overlap'
SCORE_METHOD = 'score'
TWEETS_COLLECTION = 'tweets'
WEBPAGES_COLLECTION = 'webpages'
TWEETS_SUBSAMPLE = 'sample_tweets'
WEBPAGES_SUBSAMPLE = 'sample_webpages_test'


def query(uri, gather_func, score_funcs, tweets_coll, webpages_coll, limit=0):
    webpage = webpages_coll.find_one(dict(url=uri))
    if not webpage:
        #XXX webpage not found?  put it into the pipeline
        raise NotImplementedError

    tweets = call_asmuch(gather_func, dict(
        url = uri,
        webpage = webpage,
        tweets = tweets_coll,
        webpages = webpages_coll,
    ))
    if tweets is None:
        raise TypeError(
            "gathering step did not yield result collection; missing return?")
    elif not tweets:
        return []  # exit early
    
    ranking = Queue.PriorityQueue(limit)    
    for tweet in tweets:                      
        score = sum(call_asmuch(score_func, dict(
            tweet = tweet,
            url = uri,
            webpage = webpage,
            tweets = tweets_coll,
            webpages = webpages_coll,
        )) for score_func in score_funcs)        
        if not ranking.full():
            ranking.put((score, tweet))
        elif score > ranking.queue[0][0]:            
            ranking.get()
            ranking.put((score, tweet))    
    return ranking.queue

def load_component(package, module, component):
    mod = import_module(package + '.' + module)
    return getattr(mod, component)


def run(url, gatherer, rankers, tweets_ref, webpages_ref, limit=0):
    """Wrapper upon `query` which handles textual references to the gather/rank
    components and the tweets/webpages collection.

    """
    gather_func = load_component(GATHER_PACKAGE, gatherer, GATHER_METHOD)
    score_funcs = [load_component(SCORE_PACKAGE, ranker, SCORE_METHOD)
                   for ranker in rankers]

    tweets_coll = mongo.db[tweets_ref]
    webpages_coll = mongo.db[webpages_ref]
    
    return query(url,
                 gather_func, score_funcs, tweets_coll, webpages_coll, limit)


def main(args=None):
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description = 'Find relevant tweets for an URL.',
    )

    parser.add_argument('url', metavar='URL',
            help="News article.")
    parser.add_argument('--gather', default=GATHER_MODULE, metavar='COMPONENT',
            help="tweetRecommender/gather/*.py, default: %(default)s")
    parser.add_argument('--rank', action='append', metavar='COMPONENT',
            help="tweetRecommender/rank/*.py, default: %(default)s")
    parser.add_argument('--tweets', metavar='COLLECTION',
            default=TWEETS_COLLECTION,
            help="MongoDB collection containing tweets")
    parser.add_argument('--webpages', metavar='COLLECTION',
            default=WEBPAGES_COLLECTION,
            help="MongoDB collection containing news articles")
    parser.add_argument('--sample', nargs=0, action=set_vars(
            tweets = TWEETS_SUBSAMPLE, webpages = WEBPAGES_SUBSAMPLE),
            help="same as --tweets=%s --webpages=%s" %
            (TWEETS_SUBSAMPLE, WEBPAGES_SUBSAMPLE))
    parser.add_argument('--top', dest='limit', metavar='k', type=int,
            help="maximum number of results")
    parser.add_argument('--show-score', action='store_true',
            help="show scores alongside tweets")    
    parser.add_argument('--evaluate', action='store_true',
            help="compares result with gold standard")    

    try:
        args = parser.parse_args(args=args)
    except argparse.ArgumentError:
        parser.print_help()
        return 1
    if not args.rank:               # cannot set as default=
        args.rank = [SCORE_MODULE]  # because action=append

    try:
        tweets = run(url=args.url, limit=args.limit,
            gatherer=args.gather, rankers=args.rank,
            tweets_ref=args.tweets, webpages_ref=args.webpages)
    except Exception, e:
        import traceback
        traceback.print_exc()
        return 2
    for score, tweet in tweets:
        if args.show_score:
            print("[%.3f] " % (score,), end='')
        print(u"@%s: %s" %
                (tweet['user']['screen_name'], tweet['text'].encode("ascii", "ignore")))
    if args.evaluate:
        evaluate_query(args.url, tweets)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
