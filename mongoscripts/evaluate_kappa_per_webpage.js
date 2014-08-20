// Fleiss' kappa
var N = {};
db.evaluation.aggregate([
  {$group: {_id: {t: '$tweet', w: '$webpage'}, webpage: {$min: '$webpage'}, ratings: {$sum: 1}}},
  {$match: {ratings: {$gt: 1}}},
  {$group: {_id: '$webpage', count: {$sum: 1}}},
]).forEach(function(num) {
  N[num._id] = num.count;
});

var kappa = {};
db.evaluation.aggregate([
  {$group: {
    _id: {t: '$tweet', w: '$webpage'},
    webpage: {$min: '$webpage'},
    positive: {$sum: {$cond: {if: {$eq: ['$rating', +1]}, then: 1, else: 0}}},
    negative: {$sum: {$cond: {if: {$eq: ['$rating', -1]}, then: 1, else: 0}}},
    ratings: {$sum: 1}, // n
  }},
  {$match: {
    ratings: {$gt: 1},
  }},
  {$group: {
    _id: '$webpage',
    // ∑ (positive² + negative² - ratings) / [ratings * (ratings - 1)]
    Pmean: {$sum:
      {$divide: [
        {$subtract: [
          {$add: [
            {$multiply: ['$positive', '$positive']},
            {$multiply: ['$negative', '$negative']},
          ]},
          '$ratings',
        ]},
        {$multiply: ['$ratings', {$subtract: ['$ratings', 1]}]},
      ]},
    },
    ppos: {$sum: {$divide: ['$positive', '$ratings']}},
    pneg: {$sum: {$divide: ['$negative', '$ratings']}},
    n: {$sum: '$ratings'},
  }},
]).forEach(function(result) {
  var n = N[result._id];
  var Pmean = result.Pmean / n;
  var Pchance = (Math.pow(result.ppos / n, 2) + Math.pow(result.pneg / n, 2));
  var k = (Pmean - Pchance) / (1 - Pchance);
  kappa[result._id.replace(/.*\/(.*)\?.*/, "$1")] = k;
  print(k + "," + result.n);
});
// tail -n +3 | gnuplot -e 'set term png; set datafile separator ","; set output "| see image/png:-"; set arrow 1 from 0,0.41 to 410,0.41 nohead; set xrange [0:410]; set nokey; plot "-" using 2:1'
