from __future__ import print_function, division

from tweetRecommender.mongo import mongo
from tweetRecommender import query
from tweetRecommender.gather import terms, urlmatching
from tweetRecommender.filter import expected_time


WEBPAGES_COLLECTION = 'sample_webpages'
TWEETS_COLLECTION = 'sample_tweets'
FILTERS = []
# FILTERS = [expected_time.filter]

def main():
    overlaps = []
    subsets = 0
    try:
        while 1:
            coll = mongo.coll(TWEETS_COLLECTION)
            webpage = mongo.random(WEBPAGES_COLLECTION)
            webid = webpage['_id']

            terms_gathered = set(t['tweet_id'] for t in
                    query.gather(webpage, terms.gather, FILTERS, [], coll))
            if not terms_gathered:
                print("(bail) [{0}]".format(webid))
                continue

            url_gathered = set(t['tweet_id'] for t in
                    query.gather(webpage, urlmatching.gather, FILTERS, [], coll))
            nurls = len(url_gathered)

            overlap = len(terms_gathered.intersection(url_gathered))
            overlaps.append(overlap / nurls)

            if overlap == nurls:
                subsets += 1

            print("({3:03.0f}%) terms {0:06d} ({1}) {2} urlmatching  [{4}]".format(
                len(terms_gathered), overlap, nurls, overlap / nurls * 100, webid))
    except KeyboardInterrupt:
        print(" abort after", len(overlaps))
        print("total:", sum(overlaps) / len(overlaps))
        print("strict subsets:", subsets / len(overlaps))

if __name__ == '__main__':
    import sys
    main()
