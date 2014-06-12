import six

def vote(rankings, weights):
    """Determine an overall ranking between several voters."""
    # Borda count
    overall = {}
    count = len(rankings[0])
    for ranking, weight in zip(rankings, weights):
        ties = 0
        last_score = float('nan')
        for pos, (score, item) in enumerate(ranking):
            if score == last_score:
                ties += 1
            current = overall.get(item, 0)
            overall[item] = current + (count - pos + ties) * weight
            last_score = score
    return ((score, tweet) for tweet, score in six.iteritems(overall))
