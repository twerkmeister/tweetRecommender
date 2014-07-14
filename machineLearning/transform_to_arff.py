from tweetRecommender.mongo import mongo

import os

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
        output.write("@ATTRIBUTE %s NUMERIC\n" % ranker)

    output.write("@DATA\n")

    x = mongo.coll("evaluation").aggregate({"$group": {
        "_id": "$webpage",
        "positive": {"$sum": {"$cond": {"if": {"$eq": ["$rating", +1]}, "then": 1, "else": 0}}},
        "negative": {"$sum": {"$cond": {"if": {"$eq": ["$rating", -1]}, "then": 1, "else": 0}}},
    }})
    print x

