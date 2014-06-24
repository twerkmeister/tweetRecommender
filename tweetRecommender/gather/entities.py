from kales import Kales
from tweetRecommender.tokenize import get_terms

DISPLAY_NAME = "Entity matching"

#entities extraction using opencalais
API_KEY = "yzutnbsbs668m3qepb5khwxm"
num_of_entities = 10
def gather(webpage):
    kales = Kales(API_KEY)
    data = kales.analyze(webpage['content'].encode('utf-8'))
    terms = list()    
    entity_tuples= [(entity['relevance'], entity['name'])for entity in data["entities"]]        
    for entity in sorted(entity_tuples, key=lambda entity: entity[0], reverse=True)[:num_of_entities]: #sort by relevance
        terms.extend(get_terms(entity[1]))            
    return {'terms': {'$in': terms}}
