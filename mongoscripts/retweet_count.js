// vim:sw=2
var coll = 'sample_tweets';
printjson(db[coll].mapReduce(
  function() {
    emit(this.retweeted_status.id, 1);
  },
  function(key, values) {
    return values.length;
  },
  {
    query: {retweeted_status: {$exists: 1}},
    out: {merge: coll}
  }
));
