
db.evaluation_cache_fresh.find().forEach(function(cachedResult){
  cachedResult.tweet_list.forEach(function(tweet){
    db.evaluation.find({webpage: cachedResult.query_url, tweet:tweet.tweet._id + ""}).forEach(function(evaluation){
      evaluation.scores = {}
      evaluation.scores.lda_cossim = tweet.scores[0].lda_cossim
      evaluation.scores.language_model = tweet.scores[1].language_model
      evaluation.scores.text_overlap = tweet.scores[2]["text_overlap"]
      evaluation.tweet_length = tweet.tweet.terms.length
      db.evaluation_enriched.insert(evaluation)
    });
  });
});