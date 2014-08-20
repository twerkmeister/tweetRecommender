function get_absolute_time(webpage_creation_time, tweet_creation_time) {
  return Math.abs(webpage_creation_time - tweet_creation_time)
}

function get_relative_time(webpage_creation_time, tweet_creation_time) {
  return tweet_creation_time - webpage_creation_time
}

function get_binary_time_decision(webpage_creation_time, tweet_creation_time) {
  // webpage published... (-1: before, 1: after)
  if (tweet_creation_time - webpage_creation_time) >= 0
    return 1
  return -1
}

function get_capped_time(webpage_creation_time, tweet_creation_time) {
  // return 0 for all tweets published before webpage and real value for other
  if (tweet_creation_time - webpage_creation_time) > 0
    return (tweet_creation_time - webpage_creation_time)
  return 0
}

function get_time_values(query_url, tweet_creation_time) {
  webpage_creation_time = db.sample_webpages.findOne({url: query_url}).created_at
  time_values = {}
  time_values.absolute_time_difference = get_absolute_time(webpage_creation_time, tweet_creation_time)
  time_values.relative_time_difference = get_relative_time(webpage_creation_time, tweet_creation_time)
  time_values.binary_decision = get_binary_time_decision(webpage_creation_time, tweet_creation_time) 
  time_values.capped_time_after = get_capped_time(webpage_creation_time, tweet_creation_time)
  return time_values
}

db.evaluation_cache_advanced.find().forEach(function(cachedResult){
  cachedResult.tweet_list.forEach(function(tweet){
    db.evaluation.find({webpage: cachedResult.query_url, tweet:tweet.tweet._id + ""}).forEach(function(evaluation){
      evaluation.scores = {}
      evaluation.scores.lda_cossim = tweet.scores[0].lda_cossim
      evaluation.scores.language_model = tweet.scores[1].language_model
      evaluation.tweet_length = tweet.tweet.terms.length // number of terms after stopword removal and stemming
      evaluation.chars = tweet.tweet.text.length
      evaluation.times = get_time_values(cachedResult.query_url, tweet.tweet.created_at)
      db.evaluation_enriched.insert(evaluation)
    });
  });
});

