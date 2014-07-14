db.evaluation.aggregate([
  {$group: {
    _id: '$tweet',
    ratings: {$sum: 1},
    positive: {$sum: {$cond: {if: {$eq: ["$rating", +1]}, then: 1, else: 0}}},
    negative: {$sum: {$cond: {if: {$eq: ["$rating", -1]}, then: 1, else: 0}}},
  }},
  {$sort: {ratings: 1}},
]).forEach(function(t) { printjson(t); });
