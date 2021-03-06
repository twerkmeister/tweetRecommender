db.tweets.ensureIndex({full_urls: 1})  // multikey
db.tweets.ensureIndex({hashtags: 1})  // multikey

db.sample_tweets.ensureIndex({terms: 1})  // multikey
db.sample_tweets.ensureIndex({hashtags: 1})
db.sample_tweets.ensureIndex({full_urls: 1})
db.sample_tweets.ensureIndex({created_at: 1})
db.sample_tweets.ensureIndex({created_at: 1, terms: 1})

db.webpages.ensureIndex({url: "hashed"})
db.redirects.ensureIndex({from: "hashed"})
