from collections import namedtuple
from datetime import timedelta

Threshold = namedtuple('Threshold', 'name delta desc')

THRESHOLDS = [
    Threshold('hour',   timedelta(0, 3600), 'An hour'),
    Threshold('day',    timedelta(1,),      '1 day'),
    Threshold('week',   timedelta(7,),      '1 week'),
    Threshold('month',  timedelta(31,),     '1 month'),
    Threshold('month3', timedelta(91,),     '3 months'),
    Threshold('month6', timedelta(182,),    '6 months'),
    Threshold('year',   timedelta(365,),    'A year'),
]
