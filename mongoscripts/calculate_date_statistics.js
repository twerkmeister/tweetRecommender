db = connect("localhost:27017/twitter_subset");
db.auth("mpss14n", "twitter")

var map = function(){ 
  for(var idx = 0; idx < this.full_urls.length; idx++){
    emit(this.full_urls[idx], this.created_at);
  }
};

var reduce = function(url, timestamps){
  var summary = {avg: 0, max: 0, min: 0, count: timestamps.length};
  timestamps.sort().reverse();
  var reference = timestamps.pop()
  for (var idx = 0; idx < timestamps.length; idx++){
    var distance = (timestamps[idx] - reference);
    summary.avg += distance/timestamps.length;
    if(distance > summary.max) {
      summary.max = distance;
    }
    if(summary.min == 0 || summary.min > distance){
      summary.min = distance;
    }
  }
  return summary;
};

var finalizeF = function(key, summary){
  if(!summary.avg){
    return {avg: 0, max: 0, min: 0, count: 1}
  }
  else{
    return summary
  }
}

db.sample_tweets.mapReduce(map, reduce, {out: "time_distances", finalize: finalizeF});


var distances = db.time_distances.find({"value.count" : {$gt: 2}, "value.avg" : {$gt: 0}, "value.max": {$gt: 0}, "value.min": {$gt:0}})
var count = distances.count()
print(count)
var distances = db.time_distances.find({"value.count" : {$gt: 2}, "value.avg" : {$gt: 0}, "value.max": {$gt: 0}, "value.min": {$gt:0}})
var stats = {expectancy: 0, variance: 0, standardDeviation: 0};

while(distances.hasNext()){
  value = distances.next();
  stats.expectancy += value.value.avg / (1000 * 3600);
}
stats.expectancy = stats.expectancy / count

var distances = db.time_distances.find({"value.count" : {$gt: 2}, "value.avg" : {$gt: 0}, "value.max": {$gt: 0}, "value.min": {$gt:0}})
while(distances.hasNext()){
  value = distances.next();
  stats.variance += Math.pow((value.value.avg / (1000*3600)) - stats.expectancy, 2) / count;
}
stats.standardDeviation = Math.sqrt(stats.variance)

printjson(stats);