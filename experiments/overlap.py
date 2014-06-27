from tweetRecommender.mongo import mongo
import bson.code

terms = ['carney', 'campaignfin', 'play', 'execut', 'show', 'offici', 'alway',
'highcost', 'legal', 'increasingli', 'tough', 'mixedus', 'involv', 'despit',
'privat', 'republican', 'fec', 'advantag', 'jay', 'tv', 'lo', 'former', 'late',
'offic', 'busi', 'decis', 'sens', 'he', 'donat', 'chairman', 'earli', 'anim',
'hit', 'nearli', 'variou', 'format', 'ceo', 'reagan', 'stop', '50minut',
'nation', 'strategist', 'feder', 'jack', 'govern', 'foot', 'one', 'day',
'requir', 'tri', 'administr', 'outstand', 'f', 'democrat', 'nontradit',
'secretari', 'benefit', 'presidenti', 'kennedi', 'fallon', 'view', 'easygo',
'outpac', 'set', 'hell', 'cabl', 'back', 'go', 'see', 'cost', 'result', 'year',
'resourc', 'commiss', 'event', 'pete', 'wire', 'appear', 'rate', 'reform',
'per', 'mason', 'health', 'staffer', 'deficit', 'reader', 'boost', 'leader',
'never', 'reach', 'million', 'lodg', 'host', 'california', 'promot', 'address',
'news', 'along', 'pleasur', 'come', '20vehicl', 'spoke', 'legitim', 'last',
'easi', 'invit', 'alon', 'aircraft', 'david', 'megafundrais', 'polici',
'dinner', 'place', 'presid', 'sepp', 'studio', 'industri', 'reimburs', 'first',
'oper', 'theyr', 'there', 'elect', 'campaign', 'point', 'press', 'tuesday',
'newspap', 'washington', 'likabl', 'latenight', 'doesnt', 'done', 'coverag',
'laugh', 'bonjean', 'total', 'taxpay', 'motorcad', 'use', 'certainli', 'guest',
'commun', 'pendleton', 'likelihood', 'night', 'question', 'two', 'jimmi',
'secret', 'necessarili', 'includ', 'way', 'talkshow', 'taken', 'white', 'john',
'want', 'lowest', 'tradit', 'flight', 'lot', 'forc', 'imag', 'emphas',
'broadcast', 'partli', 'actual', 'anybodi', 'effort', 'analyst', 'obama',
'case', '10', 'made', 'hour', 'hous', '18']

COLL = 'sample_tweets'
# COLL = 'tweets'
TRESHOLD = 5

intersection_js = '''
function intersection(x, y){
  var z = 0;
  for (var i = 0; i < x.length; i++) {
    for (var j = 0; j < y.length; j++) {
      if (x[i] == y[j]) {
        z++;
        break;
      }
    }
  }
  return z;
}
'''

terms_clause = '''
function() {
    var match = intersection(terms, this.terms);
    return match >= treshold;
}
'''
#  this.terms.filter(function(n) {
#         return terms.indexOf(n) != -1
#  });

where_clause = bson.code.Code(terms_clause, dict(
    intersection = bson.code.Code(intersection_js),
    terms = terms,
    treshold = TRESHOLD,
))


cursor = mongo.coll(COLL).find({
    'terms': {'$in': terms},
    '$where': where_clause,
})
print cursor
for i, t in enumerate(cursor):
    pass
print i
