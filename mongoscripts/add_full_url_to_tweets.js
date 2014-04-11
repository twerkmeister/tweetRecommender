db = connect("localhost:27017/twitter_subset");

var cursor = db.tweets.find();

var re = /(https?:\/\/)?(www.)?([A-Za-z0-9-\.]+)\/?/;

while(cursor.hasNext()){
  var t = cursor.next();
  t.better_urls = [];
  for(var i = 0; i < t.urls.length; i++){
    redirect = db.redirects.findOne({from: t.urls[i]});
    if(redirect){
      t.better_urls.push({
        "short": t.urls[i],
        "long": redirect.to,
        "domain": redirect.to.match(re)[3]
      })
    }
    //The following does not really work because some redirects are simply missing
    // else{
    //   t.beeter_urls.push({
    //     "long": t.urls[i]
    //     "domain": redirect.
    //   })
    // }
  }
  db.tweets.save(t);
}

