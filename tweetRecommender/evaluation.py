from __future__ import division
from tweetRecommender.mongo import mongo
from tweetRecommender import query

def gold_standard(uri):
    return mongo.coll("sample_tweets").find({"full_urls": uri})

def evaluate_webpage(uri):
    reference = [tweet["_id"] for tweet in gold_standard(uri)]
    result = query.query(uri)

    found = 0
    combined_score = 0

    for score, tweet in result:
        if tweet["_id"] in reference:
            found += 1
            combined_score += score

    precision = found / len(result)
    recall = found / len(reference)

    print uri + ":"
    print len(reference), "relevant tweets", "-", found, "found tweets"
    print (precision, recall), "(precision, recall)"
    print "\n"

    return (precision, recall)

def get_testset():
    return mongo.coll("sample_webpages_test").find()

def main():
    testset = get_testset()
    total = (0, 0)
    result = []
    for doc in testset:
        tmp = evaluate_webpage(doc["url"])
        result.append(tmp)
        total = (total[0] + tmp[0], total[1] + tmp[1])

    print "Average precision:", total[0] / testset.count()
    print "Average recall:", total[1] / testset.count()

    result.sort(key=lambda pair: pair[0], reverse=True)
    print "Max precision:", result[0][0]

    result.sort(key=lambda pair: pair[1], reverse=True)
    print "Max recall:", result[0][1]

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print evaluate_webpage(sys.argv[1])
    else:
        main()