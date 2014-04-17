db.webpages_tweets.ensureIndex({url: "hashed"})
db.webpages.ensureIndex({url: "hashed"})
db.redirects.ensureIndex({from: "hashed"})
