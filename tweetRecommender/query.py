#!/usr/bin/env python

from __future__ import print_function
import argparse
import itertools
import logging
import operator
import Queue

from tweetRecommender.mongo import mongo
from tweetRecommender.util import call_asmuch, set_vars
from tweetRecommender.machinery import load_component, find_components


GATHER_PACKAGE = 'tweetRecommender.gather'
GATHER_MODULE = 'terms'
GATHER_METHOD = 'gather'
SCORE_PACKAGE = 'tweetRecommender.rank'
SCORE_MODULES = ['text_overlap']
SCORE_METHOD = 'score'
SCORE_INFO_FIELDS = 'FIELDS'
FILTER_PACKAGE = 'tweetRecommender.filter'
FILTER_MODULES = ['expected_time']
FILTER_METHOD = 'filter'

#XXX maybe use config values?
TWEETS_COLLECTION = 'tweets'
WEBPAGES_COLLECTION = 'webpages'
TWEETS_SUBSAMPLE = 'sample_tweets'
WEBPAGES_SUBSAMPLE = 'sample_webpages_test'


def query(uri, gather_func, score_funcs, filter_funcs, projection,
          tweets_coll, webpages_coll, limit=0):
    logging.info("Querying for %s..", uri)
    webpage = webpages_coll.find_one(dict(url=uri))
    if not webpage:
        #XXX webpage not found?  put it into the pipeline
        raise NotImplementedError

    logging.info("Retrieving criteria from %s.%s..", gather_func.__module__, gather_func)
    find_criteria = call_asmuch(gather_func, dict(
        url = uri,
        webpage = webpage,
        tweets = tweets_coll,
        webpages = webpages_coll,
    ))

    if find_criteria is None:
        raise TypeError(
            "gathering step did not yield result criteria; missing return?")
    logging.info("Criteria: %s", find_criteria)

    for filter_func in filter_funcs:
        logging.info("Filtering query with %s.%s..", filter_func.__module__, filter_func)
        new_criteria = call_asmuch(filter_func, dict(
            url = uri,
            webpage = webpage,
        ))
        logging.info("New criteria: %s", new_criteria)
        find_criteria.update(new_criteria)

    custom_fields = ", ".join("`%s'"%p for p in projection)
    projection.add('tweet_id')
    projection.add('user.screen_name')
    projection.add('text')
    logging.info("Retrieving tweets with fields %s..", custom_fields)
    tweets = tweets_coll.find(find_criteria, dict.fromkeys(projection, 1))

    logging.info("Counting tweets..")
    count = tweets.count()  #XXX ugh!
    if not count:
        logging.info("No tweets retrieved; abort.")
        return []  # exit early
    logging.info("Counted %d tweets.", count)

    nvotes = len(score_funcs)
    rankings = [Queue.PriorityQueue(count)
                for _ in range(nvotes)]
    logging.info("Scoring by %s..", ", ".join("%s.%s" % (s.__module__, s)
        for s in score_funcs))
    tweets_index = {}
    for tweet in tweets:
        key = tweet['tweet_id']
        tweets_index[key] = dict(
                user = tweet['user']['screen_name'],
                text = tweet['text'],
                id = key,
        )
        for score_func, ranking in zip(score_funcs, rankings):
            score = call_asmuch(score_func, dict(
                tweet = tweet,
                url = uri,
                webpage = webpage,
                tweets = tweets_coll,
                webpages = webpages_coll,
            ))
            if not ranking.full():
                ranking.put((score, key))
            elif score > ranking.queue[0][0]:
                ranking.get()
                ranking.put((score, key))

    # Borda count
    if nvotes == 1:
        logging.info("Skipped voting;  monarchy.")
        overall = ((tweet, score) for score, tweet in ranking.queue)
    else:
        logging.info("Voting..")
        overall = {}
        for ranking in rankings:
            for pos, (score, tweet) in enumerate(ranking.queue):
                current = overall.get(tweet, 0)
                overall[tweet] = current + count - pos
        overall = overall.items()

    logging.info("Sorting..")
    #XXX consider ties
    return [(score, tweets_index[tweet]) for tweet, score in
            sorted(overall,
                   key=operator.itemgetter(1), reverse=True)[:limit]]


def run(url, gatherer, rankers, filters, tweets_ref, webpages_ref, limit=0):
    """Wrapper upon `query` which handles textual references to the gather/rank
    components and the tweets/webpages collection.

    """
    gather_func = load_component(GATHER_PACKAGE, gatherer, GATHER_METHOD)
    if not hasattr(rankers, '__iter__'):
        rankers = [rankers]  # backwards compat
    score_funcs = [load_component(SCORE_PACKAGE, ranker, SCORE_METHOD)
                   for ranker in rankers]
    fields = set(itertools.chain(*[load_component(SCORE_PACKAGE, ranker, SCORE_INFO_FIELDS)
                      for ranker in rankers]))
    filter_funcs = [load_component(FILTER_PACKAGE, filter_, FILTER_METHOD)
                    for filter_ in filters]

    tweets_coll = mongo.db[tweets_ref]
    webpages_coll = mongo.db[webpages_ref]

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

    logging.basicConfig(level=logging.INFO)

    try:
        tweets = run(url=args.url, limit=args.limit,
            gatherer=args.gather, rankers=args.rank, filters=args.filters,
            tweets_ref=args.tweets, webpages_ref=args.webpages)
    except Exception, e:
        import traceback
        traceback.print_exc()
        return 2
    digits = len(str(int(tweets[0][0])))
    score_format = ".2f" if len(args.rank) == 1 else "0%sd" % digits
    score_format = ("%%%s," if args.raw else "[%%%s] ") % score_format
    tweet_format = (u"%(id)s" if args.raw else u"@%(user)s: %(text)s")
    for score, tweet in tweets:
        tweet['text'] = tweet['text'].encode('ascii', 'ignore')
        if args.show_score:
            print(score_format % (score,), end='')
        print(tweet_format % tweet)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
