from tweetRecommender.mongo import mongo

import os
from bson import ObjectId

script = """var x = db.evaluation.aggregate([
 {$group: {
  _id: "$webpage",
  positive: {$sum: {$cond: {if: {$eq: ["$rating", +1]}, then: 1, else: 0}}},
  negative: {$sum: {$cond: {if: {$eq: ["$rating", -1]}, then: 1, else: 0}}},
 }},
])

print x"""

EVALUATION_RANKERS = ['lda_cossim', 'language_model', 'text_overlap_plus_normalized_follower_count']
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output/evaluation.arff")

with open(OUTPUT_PATH, "w") as output:
    output.write("@RELATION ratings\n")

    for ranker in EVALUATION_RANKERS:
        output.write("@ATTRIBUTE %s real\n" % ranker)

    output.write("@ATTRIBUTE rating {yes,no}\n")
    output.write("@DATA\n")

    x = mongo.coll("evaluation").aggregate([{"$group": {
        "_id": { "webpage": "$webpage", "tweet": "$tweet" },
        "positive": {"$sum": {"$cond": {"if": {"$eq": ["$rating", +1]}, "then": 1, "else": 0}}},
        "negative": {"$sum": {"$cond": {"if": {"$eq": ["$rating", -1]}, "then": 1, "else": 0}}},
    }},
    {"$group": {
        "_id": "$_id.webpage",
        "tweets": {"$push": {
            "tweet": "$_id.tweet",
            "positive": "$positive",
            "negative": "$negative"
        }}
    }}])

    for webpage in x["result"]:
        query_url = webpage["_id"]
        for tweet in webpage["tweets"]:
            cache = mongo.coll("evaluation_cache_advanced").find_one(
                {"query_url": query_url}, 
                {"tweet_list": {"$elemMatch": {"tweet._id": ObjectId(tweet["tweet"])}}}
            )

            for score in cache["tweet_list"][0]["ranks"]:
                if score.keys()[0] == "lda_cossim":
                    value1 = score.values()[0]
                elif score.keys()[0] == "language_model":
                    value2 = score.values()[0]
                else:
                    value3 = score.values()[0]

            rating = "no"
            if tweet["positive"] > tweet["negative"]:
                rating = "yes"

            output.write("%d,%d,%d,%s\n" % (value1, value2, value3, rating))


