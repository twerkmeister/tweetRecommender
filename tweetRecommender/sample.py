import random
from tweetRecommender.mongo import mongo

try:
    xrange
except NameError:
    pass
else:
    range = xrange

def random_sample(num_items, source_coll, target_coll):
    source = mongo.coll(source_coll)
    target = mongo.coll(target_coll)

    population = source.count()
    ids = random.sample(range(population), num_items)

    #XXX use $in
    for i in ids:
        doc = source.find().skip(i).limit(1)
        target.insert(doc)
