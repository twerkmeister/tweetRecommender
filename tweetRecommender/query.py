#!/usr/bin/env python

from __future__ import print_function
import argparse
import itertools
import logging
import operator
import Queue

from tweetRecommender.machinery import load_component, find_components
from tweetRecommender.mongo import mongo
from tweetRecommender.util import set_vars

from six import string_types


GATHER_PACKAGE = 'tweetRecommender.gather'
GATHER_MODULE = 'terms'
GATHER_METHOD = 'gather'
SCORE_PACKAGE = 'tweetRecommender.rank'
SCORE_MODULES = ['text_overlap']
SCORE_METHOD = 'score'
SCORE_INFO_FIELDS = 'fields'
FILTER_PACKAGE = 'tweetRecommender.filter'
FILTER_MODULES = ['expected_time']
FILTER_METHOD = 'filter'

#XXX maybe use config values?
TWEETS_COLLECTION = 'tweets'
WEBPAGES_COLLECTION = 'webpages'
TWEETS_SUBSAMPLE = 'sample_tweets'
WEBPAGES_SUBSAMPLE = 'sample_webpages_test'

LOG = logging.getLogger('tweetRecommender.query')


def query(uri, gather_func, score_funcs, filter_funcs, fields,
          tweets_coll, webpages_coll, limit):
    LOG.info("Querying for %s..", uri)
    webpage = webpages_coll.find_one(dict(url=uri))
    if not webpage:
        #XXX webpage not found?  put it into the pipeline
        raise NotImplementedError

    required_fields = _required_fields(score_funcs).union(fields)

    tweets = gather(webpage, gather_func, filter_funcs,
                    required_fields, tweets_coll)
    return rank(tweets, score_funcs, webpage, limit)

def gather(webpage, gather_func, filter_funcs, required_fields, coll):
    LOG.info("Retrieving criteria from %s.%s..",
            gather_func.__module__, gather_func)
    find_criteria = gather_func(webpage)

    if find_criteria is None:
        raise TypeError(
            "gathering step did not yield result criteria; missing return?")
    LOG.info("Criteria: %s", find_criteria)

    for filter_func in filter_funcs:
        LOG.info("Filtering query with %s.%s..",
                filter_func.__module__, filter_func)
        new_criteria = filter_func(webpage)
        LOG.info("New criteria: %s", new_criteria)
        #XXX merge conflicts (overridden fields)
        find_criteria.update(new_criteria)

    LOG.info("Retrieving tweets with fields %s..",
                 ", ".join("`%s'"%p for p in required_fields))
    required_fields.add('tweet_id')

    tweets = coll.find(find_criteria, dict.fromkeys(required_fields, 1))
    return tweets

def rank(tweets, score_funcs, webpage, limit):
    LOG.debug("Counting tweets..")
    count = tweets.count()  #XXX ugh!
    if not count:
        LOG.warning("No tweets retrieved; abort.")
        return []  # exit early
    LOG.info("Counted %d tweets.", count)

    nvotes = len(score_funcs)
    window = count if nvotes > 1 else limit
    rankings = [Queue.PriorityQueue(window)
                for _ in range(nvotes)]
    LOG.info("Scoring by %s..",
            ", ".join("%s.%s" % (s.__module__, s) for s in score_funcs))
    tweets_index = {}
    zip_score_rank = list(zip(score_funcs, rankings))
    for tweet in tweets:
        key = tweet['tweet_id']
        tweets_index[key] = tweet #XXX minimize
        for score_func, ranking in zip_score_rank:
            score = score_func(tweet, webpage)
            if not ranking.full():
                ranking.put((score, key))
            elif score > ranking.queue[0][0]:
                ranking.get()
                ranking.put((score, key))

    if nvotes == 1:
        LOG.info("Skipped voting;  monarchy.")
        overall = ((tweet, score) for score, tweet in ranking.queue)
    else:
        LOG.debug("Voting..")
        # Borda count
        overall = {}
        for ranking in rankings:
            for pos, (score, tweet) in enumerate(ranking.queue):
                current = overall.get(tweet, 0)
                overall[tweet] = current + count - pos
        overall = overall.items()

    LOG.debug("Sorting..")
    #XXX consider ties
    return [(score, tweets_index[tweet]) for tweet, score in
            sorted(overall, key=operator.itemgetter(1), reverse=True)[:limit]]

def _required_fields(funcs):
    fields = set()
    for func in funcs:
        fields.update(getattr(func, SCORE_INFO_FIELDS))
    return fields


def run(url, gatherer, rankers, filters,
        fields, tweets_ref, webpages_ref, limit):
    """Wrapper upon `query` which handles textual references to the gather/rank
    components and the tweets/webpages collection.

    """
    gather_func = load_component(GATHER_PACKAGE, gatherer, GATHER_METHOD)
    if isinstance(rankers, string_types):
        rankers = [rankers]  # backwards compat
    score_funcs = [load_component(SCORE_PACKAGE, ranker, SCORE_METHOD)
                   for ranker in rankers]
    filter_funcs = [load_component(FILTER_PACKAGE, filter_, FILTER_METHOD)
                    for filter_ in filters]

    tweets_coll = mongo.coll(tweets_ref)
    webpages_coll = mongo.coll(webpages_ref)

    return query(url, gather_func, score_funcs, filter_funcs, fields,
                 tweets_coll, webpages_coll, limit)


def main(args=None):
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description = 'Find relevant tweets for an URL.',
    )

    parser.add_argument('url', metavar='URL',
            help="News article.")
    parser.add_argument('--gather', default=GATHER_MODULE, metavar='COMPONENT',
            help="%s/*.py, default: %%(default)s" %
            (GATHER_PACKAGE.replace('.', '/'),))
    parser.add_argument('--rank', action='append', metavar='COMPONENT',
            help="%s/*.py, defaults: %s" %
            (SCORE_PACKAGE.replace('.', '/'), ', '.join(SCORE_MODULES)))
    parser.add_argument('--filter', action='append', dest='filters',
            metavar='COMPONENT', default=[],
            help="%s/*.py, defaults: %s" %
            (FILTER_PACKAGE.replace('.', '/'), ', '.join(FILTER_MODULES)))
    parser.add_argument('--no-filter', action='store_true',
            help="disable all filters")
    parser.add_argument('--tweets', metavar='COLLECTION',
            default=TWEETS_COLLECTION,
            help="MongoDB collection containing tweets (default: %(default)s)")
    parser.add_argument('--webpages', metavar='COLLECTION',
            default=WEBPAGES_COLLECTION,
            help="MongoDB collection containing news articles (default: %(default)s)")
    parser.add_argument('--sample', nargs=0, action=set_vars(
            tweets = TWEETS_SUBSAMPLE, webpages = WEBPAGES_SUBSAMPLE),
            help="same as --tweets=%s --webpages=%s" %
            (TWEETS_SUBSAMPLE, WEBPAGES_SUBSAMPLE))
    parser.add_argument('--top', dest='limit', metavar='k', type=int,
            help="maximum number of results")
    parser.add_argument('--show-score', action='store_true',
            help="show scores alongside tweets")
    parser.add_argument('--raw', action='store_true',
            help="generate machine-readable output")
    parser.add_argument('--list-components', action='store_true',
            help="list all available components")

    try:
        args = parser.parse_args(args=args)
    except argparse.ArgumentError, error:
        print("Error:", error)
        parser.print_help()
        return 1

    if args.list_components:
        if not args.raw:
            print("Available components:")
        for flag, pkg in [("gather", GATHER_PACKAGE),
                          ("filter", FILTER_PACKAGE),
                          ("rank", SCORE_PACKAGE)]:
            print("  --%s:" % flag)
            for component in find_components(pkg):
                print("\t%s" % component)
        return 0
    # cannot set as default= because action=append adds to defaults
    if not args.rank:
        args.rank = SCORE_MODULES
    if not args.filters and not args.no_filter:
        args.filters = FILTER_MODULES

    logging.basicConfig(
        level = logging.INFO,
        format = "[%(levelname)s] %(message)s",
    )

    try:
        tweets = run(url=args.url, limit=args.limit,
            gatherer=args.gather, rankers=args.rank, filters=args.filters,
            fields=['user.screen_name', 'text'],
            tweets_ref=args.tweets, webpages_ref=args.webpages)
    except Exception, e:
        import traceback
        traceback.print_exc()
        return 2

    digits = len(str(int(tweets[0][0])))
    score_format = ".2f" if len(args.rank) == 1 else "0%sd" % digits
    score_format = ("%%%s," if args.raw else "[%%%s] ") % score_format
    tweet_format = (u"{tweet_id},{user[screen_name]},{text}" if args.raw
                    else u"@{user[screen_name]}: {text}")

    for score, tweet in tweets:
        tweet['text'] = tweet['text'].encode('ascii', 'ignore')
        if args.show_score:
            print(score_format % (score,), end='')
        print(tweet_format.format(tweet))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
