from tweetRecommender.mongo import mongo
from tweetRecommender import query

def gold_standard(uri):
    tweets = mongo.coll("sample_tweets")
    tweets.find({"full_urls": uri})
    return tweets

def evaluate_webpage(uri):
    reference = gold_standard(uri)
    result = query.query(uri)

    found = 0
    combined_score = 0

    for tweet, score in result:
        if tweet in reference:
            found += 1
            combinedScore += score

    return (found, combined_score)

def testset():
    return mongo.coll("sample_webpages_test").find()

def main():
    testset = testset()
    result = []
    for doc in testset:
        result.append(evaluate_webpage(doc["url"]))

if __name__ == '__main__':
    main()