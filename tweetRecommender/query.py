#!/usr/bin/env python

from __future__ import print_function
import argparse
import operator
import Queue

from tweetRecommender.mongo import mongo
from tweetRecommender.util import call_asmuch, set_vars, load_component


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
    count = tweets.count()  #XXX ugh!
    if not count:
        return []  # exit early

    nvotes = len(score_funcs)
    #XXX is the window really correct?
    window = (count + 1) / 2 if nvotes > 1 else limit
    rankings = [Queue.PriorityQueue(window)
                for _ in range(nvotes)]
    for tweet in tweets:
        for score_func, ranking in zip(score_funcs, rankings):
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

    # Borda count
    window = max(ranking.qsize() for ranking in rankings)
    overall = {}
    for ranking in rankings:
        for pos, (score, tweet) in enumerate(ranking.queue):
            key = tweet['tweet_id']  # hashable, unique
            current = overall.get(key, [0])[0]
            #XXX consider ties
            overall[key] = (current + window - pos, tweet)
        # all unranked tweets gain 0 points

    return sorted(overall.values(),
            key=operator.itemgetter(0), reverse=True)[:limit]


def run(url, gatherer, rankers, tweets_ref, webpages_ref, limit=0):
    """Wrapper upon `query` which handles textual references to the gather/rank
    components and the tweets/webpages collection.

    """
    gather_func = load_component(GATHER_PACKAGE, gatherer, GATHER_METHOD)
    if not hasattr(rankers, '__iter__'):
        rankers = [rankers]  # backwards compat
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
            help="%s/*.py, default: %%(default)s" %
            (GATHER_PACKAGE.replace('.', '/'),))
    parser.add_argument('--rank', action='append', metavar='COMPONENT',
            help="%s/*.py, default: %%(default)s" %
            (SCORE_PACKAGE.replace('.', '/'),))
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

    try:
        args = parser.parse_args(args=args)
    except argparse.ArgumentError, error:
        print("Error:", error)
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
    digits = len(str(tweets[0][0]))
    for score, tweet in tweets:
        if args.show_score:
            print("[%0*d] " % (digits, score,), end='')
        print(u"@%s: %s" %
                (tweet['user']['screen_name'], tweet['text']))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
