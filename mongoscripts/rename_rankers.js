

db.evaluation_cache_advanced.find().forEach(function(el){el.eval.map.text_overlap_and_normalized_follower_count = el.eval.map["text_overlap, normalized_follower_count"]; db.evaluation_cache_advanced.save(el)})