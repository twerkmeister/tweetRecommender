db.webpages_tweets.ensure_index({url: "hashed"})
db.webpages.ensure_index({url: "hashed"})
db.redirects.ensure_index({from: "hashed"})
