// Fleiss' kappa
var N = db.evaluation.aggregate([
  {$group: {_id: '$tweet', ratings: {$sum: 1}}},
  {$match: {ratings: {$gt: 1}}},
  {$group: {_id: 1, count: {$sum: 1}}},
]).next().count;
var result = db.evaluation.aggregate([
  {$group: {
    _id: '$tweet',
    positive: {$sum: {$cond: {if: {$eq: ['$rating', +1]}, then: 1, else: 0}}},
    negative: {$sum: {$cond: {if: {$eq: ['$rating', -1]}, then: 1, else: 0}}},
    ratings: {$sum: 1},
  }},
  {$match: {
    ratings: {$gt: 1},
  }},
  {$group: {
    _id: 1,
    // (positive² + negative² - ratings) / [ratings * (ratings - 1)]
    Pmean: {$sum:
      {$divide: [
        {$subtract: [
          {$add: [
            {$multiply: ['$positive', '$positive']},
            {$multiply: ['$negative', '$negative']},
          ]},
          '$ratings',
        ]},
        {$multiply: [N, '$ratings', {$subtract: ['$ratings', 1]}]},
      ]},
    },
    ppos: {$sum: {$divide: ['$positive', '$ratings']}},
    pneg: {$sum: {$divide: ['$negative', '$ratings']}},
  }},
]).next();
var Pmean = result.Pmean;
var Pchance = (Math.pow(result.ppos / N, 2) + Math.pow(result.pneg / N, 2));
var kappa = (Pmean - Pchance) / (1 - Pchance);
print(N);
print(Pmean);
print(Pchance);
print("==> " + kappa);
