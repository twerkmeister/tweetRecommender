#!/usr/bin/env python

from __future__ import print_function
import argparse
from importlib import import_module
from inspect import getargspec
import operator
import Queue

from tweetRecommender.mongo import mongo


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
        raise ValueError(
            "gathering step did not yield result collection; missing return?")

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

def call_asmuch(fun, kwargs):
    args = getargspec(fun).args
    filtered_kwargs = dict((key, value) for (key, value)
            in kwargs.items() if key in args)
    return fun(**filtered_kwargs)


def main(args=None):
    parser = make_parser()
    try:
        args = parser.parse_args(args=args)
    except argparse.ArgumentError:
        parser.print_help()
        return 1
    try:
        gather_mod = import_module('tweetRecommender.gather.' + args.gather)
        gather_func = getattr(gather_mod, 'gather')
        score_mod = import_module('tweetRecommender.rank.' + args.rank)
        score_func = getattr(score_mod, 'score')
    except ImportError, e:
        #XXX log
        print("Error:", e)
        return 2
    except AttributeError, e:
        print("Error:", e)
        return 3

    tweets_coll = mongo.db[args.tweets]
    webpages_coll = mongo.db[args.webpages]

    try:
        tweets = query(args.url,
                gather_func, score_func, tweets_coll, webpages_coll)
    except Exception, e:
        #XXX log
        import traceback; traceback.print_exc()
        print("Error:", e)
        return 4

    for score, tweet in tweets[:args.limit]:
        if args.show_score:
            print("[%.3f] " % (score,), end='')
        print(u"@%s: %s" %
                (tweet['user']['screen_name'], tweet['text']))
    return 0


class set_sample_vars(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        namespace.tweets = TWEETS_SUBSAMPLE
        namespace.webpages = WEBPAGES_SUBSAMPLE

def make_parser():
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
    parser.add_argument('--sample', action=set_sample_vars, nargs=0,
            help="same as --tweets=%s --webpages=%s" %
            (TWEETS_SUBSAMPLE, WEBPAGES_SUBSAMPLE))
    parser.add_argument('--top', dest='limit', metavar='k', type=int,
            help="maximum number of results")
    parser.add_argument('--show-score', action='store_true',
            help="show scores alongside tweets")

    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())
