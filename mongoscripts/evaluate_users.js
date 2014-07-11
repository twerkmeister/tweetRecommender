db.evaluation.aggregate([
  {$group: {
    _id: "$uid",
    ratings: {$push: "$rating"},
  }}
]).forEach(function(user) {
  var num_ratings = user.ratings.length;
  var accum = new Array(num_ratings);
  accum[0] = user.ratings[0];
  for (var i = 1; i < num_ratings; i++) {
    accum[i] = accum[i-1] + user.ratings[i];
  }
  print(accum);
});
