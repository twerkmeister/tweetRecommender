def gather(url, tweets, webpages):
    return tweets.find({"full_urls": url})
