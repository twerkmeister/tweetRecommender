from __future__ import division
from math import *

DISPLAY_NAME = "Proximity to publishing date"

SECONDS_TO_DAYS_FACTOR=(1/(3600*24))
DEFAULT_SIGMA=43
DEFAULT_M=5.7
def gaussian_density(x, m=DEFAULT_M, sigma=DEFAULT_SIGMA):
  return (1/sqrt(2*pi*sigma**2)) * exp(- ((x - m) ** 2) / (2 * sigma ** 2))

def score(tweet, webpage):
  days_difference = SECONDS_TO_DAYS_FACTOR * ((tweet["created_at"] - webpage["created_at"]).total_seconds())
  return gaussian_density(days_difference)

score.fields = ['created_at']
