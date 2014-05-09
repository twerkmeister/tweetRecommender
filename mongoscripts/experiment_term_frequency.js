// vim:sw=2
var LIMIT = 10000;
var PRINT_TRESHOLD = 1;
var MINLENGTH = 3;
var HASHTAG_BLACKLIST = [
  "job",
  "jobs",
];
var BLACKLIST = [
  // depending on the MINLENGTH settings, some of these are useless
  "a",
  "about",
  "an",
  "and",
  "are",
  "as",
  "for",
  "in",
  "is",
  "my",
  "of",
  "on",
  "or",
  "our",
  "so",
  "the",
  "to",
  "we",
  "you"
];

function count(arr, elem) {
  var i = -1;
  var start = 0;
  do {
    i++;
    start = arr.indexOf(elem, start+1);
  }
  while (start != -1)
  return i;
}

function findDuplicates(arr) {
  var maxtf = 0;
  var dupes = arr.filter(function(term, pos) {
    term = term.replace(/[^a-z]/gi, '');
    if (term.length < MINLENGTH
     || !/[a-z]/i.test(term)
     || BLACKLIST.indexOf(term) != -1) {
      return;
    }
    var cnt = count(arr, term);
    if (cnt > maxtf) { maxtf = cnt; }
    return arr.indexOf(term, pos+1) != -1;
  });
  return {dupes: dupes, maxtf: maxtf};
}

var re = new RegExp("#(" + HASHTAG_BLACKLIST.join("|\b") + "\b)", "i")
var sample = db.tweets.find({text: {$not: re}}).limit(LIMIT);
var tf_gt = {};
while (sample.hasNext()) {
  var tweet = sample.next();
  var proc = findDuplicates(tweet.text.toLowerCase().split(" "));
  for (var i=0; i < proc.maxtf; i++) {
    tf_gt[i] = (tf_gt[i] || 0) + 1;
  }
  if (proc.maxtf > PRINT_TRESHOLD) {
    printjson({_id: tweet._id, text: tweet.text, dupes: proc.dupes});
  }
}
var maxtf=0;
do { maxtf++ } while (tf_gt[maxtf]);
print("--- TOTAL #DOCS PROCESSED:", LIMIT);
print("--- TOTAL #DOCS W/ DUPLICATE TERMS (TF>1):", tf_gt[1] || 0);
print("--- TOTAL #DOCS W/ TERMS, TF>2:", tf_gt[2] || 0);
print("--- MAXIMUM TF:", maxtf);
