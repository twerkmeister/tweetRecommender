from __future__ import division

from tweetRecommender.tokenize import get_terms

import bson.code

TRESHOLD = 4
CLAUSE = '''
function() {
  var c = 0
    , this_terms = this.terms
    , this_total = this.terms.length
    , terms_total = terms.length
    ;
  for (var i = 0; i < this_total; i++) {
    for (var j = 0; j < terms_total; j++) {
      if (this_terms[i] == terms[j]) {
        c++;
        break;
      }
    }
  }
  return c > treshold;
}
'''


def gather(webpage):
    terms = get_terms(webpage['content'].encode('utf-8'))
    return {
        'terms': {'$in': terms},
        '$where': bson.code.Code(CLAUSE,
            treshold = TRESHOLD,
            terms = terms,
        ),
    }
