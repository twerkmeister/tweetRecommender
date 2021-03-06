from __future__ import division
from tweetRecommender.mongo import mongo
from tweetRecommender.query import run as query

import sys

def gold_standard(uri):
    return mongo.coll("sample_tweets").find({"full_urls": uri})

def evaluate_webpage(uri):
    reference = [tweet["_id"] for tweet in gold_standard(uri)]
    result = query(uri, "terms", ["lda_cossim"], ["expected_time"], "sample_tweets", "sample_webpages_test", 10)

    found = 0
    combined_score = 0

    for score, tweet in result:
        if tweet["_id"] in reference:
            found += 1
            combined_score += score

    precision = 0.0
    if len(result) > 0:
        precision = found / len(result)
    recall = 0.0
    if len(reference) > 0:
        recall = found / len(reference)

    sys.stdout.write(uri + ":" + "\n")
    sys.stdout.write(str(len(reference)) + "relevant tweets -" + str(found) + "found tweets\n")
    sys.stdout.write("(%.2f,%.2f)" % (precision, recall))
    sys.stdout.write("(precision, recall)\n")
    sys.stdout.flush()

    return (precision, recall)

def evaluate_query(uri, tweets_results):
    reference = [tweet["_id"] for tweet in gold_standard(uri)]    
    found = 0 
    combined_score = 0    
    precision = 0.0 
    recall = 0.0
    for score, tweet in tweets_results:
        if tweet["_id"] in reference:
            found += 1
            combined_score += score    
    if len(tweets_results) > 0:
        precision = found / len(tweets_results)    
    if len(reference) > 0:
        recall = found / len(reference)
    
    print("\nevaluation result: \n")
    print(str(len(reference)) + " relevant tweets - " + str(found) + " found tweets\n")    
    print("(precision : %.2f, recall: %.2f)\n" % (precision, recall))    
    return (precision, recall)

def get_testset():
    return mongo.coll("sample_webpages_test").find(timeout=False).limit(100)

def main():
    testset = get_testset()
    total = (0, 0)
    result = []
    count = 1
    for doc in testset:
        print "Doc #", count
        count += 1
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
    if len(sys.argv) > 1:
        print evaluate_webpage(sys.argv[1])
    else:
        main()