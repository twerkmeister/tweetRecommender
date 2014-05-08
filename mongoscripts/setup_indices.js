db.tweets.ensureIndex({full_urls: 1})  // multikey
db.tweets.ensureIndex({hashtags: 1})  // multikey
db.sample_tweets.ensureIndex({terms: 1})  // multikey
db.webpages.ensureIndex({url: "hashed"})
db.redirects.ensureIndex({from: "hashed"})
