from datetime import timedelta

DISPLAY_NAME = "Expected time"

STANDARD_DEVIATION_HOURS = 43
STANDARD_EXPECTATION = 6
_SHIFT = timedelta(hours = STANDARD_EXPECTATION)
_STDDEV = timedelta(hours = STANDARD_DEVIATION_HOURS)

def filter(webpage):
    created_at = webpage['created_at'] + _SHIFT
    lower_bound = created_at - _STDDEV
    upper_bound = created_at + _STDDEV
    return {
            'created_at': {'$gt': lower_bound, '$lt': upper_bound},
           }
