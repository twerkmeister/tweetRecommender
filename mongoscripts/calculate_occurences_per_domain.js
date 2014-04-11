db = connect("localhost:27017/twitter_subset");

var cursor = db.tweets.find();

var map = function(){
  for(var i = 0; i < this.better_urls.length; i++)
    emit(this.better_urls[i].domain, 1);
}

var reduce = function(url, ones){
  return Array.sum(ones);
}

db.tweets.mapReduce(map, reduce, {out: "occurences_per_domain"})