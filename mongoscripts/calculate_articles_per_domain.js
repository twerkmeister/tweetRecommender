db = connect("localhost:27017/twitter_subset");

var map = function(){
  var re = /(https?:\/\/)?(www.)?([A-Za-z0-9-\.]+)\/?/;
  emit(this.url.match(re)[3], 1)
}

var reduce = function(domain, ones){
  return Array.sum(ones);
}

db.webpages.mapReduce(map, reduce, {out: "articles_per_domain"})