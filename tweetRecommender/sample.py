import random
from tweetRecommender.mongo import mongo

try:
    xrange
except NameError:
    pass
else:
    range = xrange

def random_sample(num_items, source_coll, target_coll):
    population = mongo.db[source_coll].count()
    ids = random.sample(range(population), num_items)
    for i in ids:
        doc = mongo.db[source_coll].find().skip(i).limit(1)
        mongo.db[target_coll].insert(doc)
