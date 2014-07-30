
db.evaluation_cache_advanced.find().forEach(function(cachedResult){
  cachedResult.tweets.forEach(function(tweet){
    db.evaluation.find({webpage: cachedResult.query_url, tweet:tweet.tweet._id + ""}).forEach(function(evaluation){
      evaluation.scores = {}
      evaluation.scores.lda_cossim = tweet.scores[0].lda_cossim
      evaluation.scores.language_model = tweet.scores[1].language_model
      evaluation.scores.text_overlap = tweet.scores[2]["text_overlap, normalized_follower_count"]
      evaluation.tweet_text = tweet.tweet.text
      db.evaluation_enriched.insert(evaluation)
    });
  });
});