from collections import namedtuple
from datetime import timedelta

Threshold = namedtuple('Threshold', 'name delta')

THRESHOLDS = [
    Threshold('hour',   timedelta(0, 3600)),
    Threshold('day',    timedelta(1,)),
    Threshold('week',   timedelta(7,)),
    Threshold('month',  timedelta(31,)),
    Threshold('month3', timedelta(91,)),
    Threshold('month6', timedelta(182,)),
    Threshold('year',   timedelta(365,)),
]
