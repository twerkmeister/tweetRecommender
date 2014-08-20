function get_absolute_time(query_url, tweet_creation_time) {
  webpage_creation_time = db.sample_webpages.findOne({url: query_url}).created_at
  return Math.abs(webpage_creation_time - tweet_creation_time)
}

db.evaluation_cache_advanced.find().forEach(function(cachedResult){
  cachedResult.tweet_list.forEach(function(tweet){
    db.evaluation.find({webpage: cachedResult.query_url, tweet:tweet.tweet._id + ""}).forEach(function(evaluation){
      evaluation.scores = {}
      evaluation.scores.lda_cossim = tweet.scores[0].lda_cossim
      evaluation.scores.language_model = tweet.scores[1].language_model
      evaluation.tweet_length = tweet.tweet.terms.length // number of terms after stopword removal and stemming
      evaluation.absolute_time_difference = get_absolute_time(cachedResult.query_url, tweet.tweet.created_at)
      db.evaluation_enriched.insert(evaluation)
    });
  });
});

