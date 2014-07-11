var cache = {};
db.evaluation_cache.find().forEach(function(result) {
  var tweets = {};
  for (var i = 0; i < result.tweets.length; i++) {
    var tweet = result.tweets[i];
    tweets[tweet.tweet._id.toString()] = tweet.scores;
  }
  cache[result.query_url] = tweets;
});

var results = {};
db.evaluation.find().forEach(function(ev) {
  var scores = cache[ev.webpage][ObjectId(ev.tweet)];
  for (var i = 0; i < scores.length; i++) {
    var ranker = Object.keys(scores[i])[0];

    var result = results[ranker];
    if (typeof result === 'undefined') {
      results[ranker] = result = {good: 0, bad: 0};
    }

    if (ev.rating == 1) { result.good++; }
    else { result.bad++; }
  }
});

Object.keys(results).forEach(function(name) {
  var ranker = results[name];
  print(name + "," + ranker.good + "," + ranker.bad)
});
