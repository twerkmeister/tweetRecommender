#!/usr/bin/env python

from __future__ import print_function
import argparse
from importlib import import_module
from inspect import getargspec
import operator
import Queue

from tweetRecommender.mongo import mongo
from tweetRecommender.util import call_asmuch, set_vars


#XXX maybe use config values?
GATHER_MODULE = 'terms'
SCORE_MODULE = 'text_overlap'
TWEETS_COLLECTION = 'tweets'
WEBPAGES_COLLECTION = 'webpages'
TWEETS_SUBSAMPLE = 'sample_tweets'
WEBPAGES_SUBSAMPLE = 'sample_webpages_test'


def query(uri, gather_func, score_func, tweets_coll, webpages_coll, limit=0):
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
        score = call_asmuch(score_func, dict(
            tweet = tweet,
            url = uri,
            webpage = webpage,
            tweets = tweets_coll,
            webpages = webpages_coll,
        ))
        if not ranking.full():
            ranking.put((score, tweet))
        elif score > ranking.queue[0][0]:
            ranking.get()
            ranking.put((score, tweet))

    return ranking.queue


def run(url, gather_comp, rank_comp, tweets_ref, webpages_ref, limit=0):
    """Wrapper upon `query` which handles textual references to the gather/rank
    components and the tweets/webpages collection.

    """
    gather_mod = import_module('tweetRecommender.gather.' + gather_comp)
    gather_func = getattr(gather_mod, 'gather')
    score_mod = import_module('tweetRecommender.rank.' + rank_comp)
    score_func = getattr(score_mod, 'score')

    tweets_coll = mongo.db[tweets_ref]
    webpages_coll = mongo.db[webpages_ref]

    return query(url,
                 gather_func, score_func, tweets_coll, webpages_coll, limit)


def main(args=None):
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description = 'Find relevant tweets for an URL.',
    )

    parser.add_argument('url', metavar='URL',
            help="News article.")
    parser.add_argument('--gather', default=GATHER_MODULE, metavar='COMPONENT',
            help="tweetRecommender/gather/*.py, default: %(default)s")
    parser.add_argument('--rank', default=SCORE_MODULE, metavar='COMPONENT',
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

    try:
        args = parser.parse_args(args=args)
    except argparse.ArgumentError:
        parser.print_help()
        return 1
    try:
        tweets = run(url=args.url, limit=args.limit,
            gather_comp=args.gather, rank_comp=args.rank,
            tweets_ref=args.tweets, webpages_ref=args.webpages)
    except Exception, e:
        import traceback
        traceback.print_exc()
        return 2
    for score, tweet in tweets:
        if args.show_score:
            print("[%.3f] " % (score,), end='')
        print(u"@%s: %s" %
                (tweet['user']['screen_name'], tweet['text']))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
