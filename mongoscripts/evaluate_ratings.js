var x = db.evaluation.aggregate([
 {$group: {
  _id: "$webpage",
  positive: {$sum: {$cond: {if: {$eq: ["$rating", +1]}, then: 1, else: 0}}},
  negative: {$sum: {$cond: {if: {$eq: ["$rating", -1]}, then: 1, else: 0}}},
 }},
])
while (x.hasNext()) {
 printjson(x.next());
}
