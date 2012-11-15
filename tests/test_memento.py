from . import TestCase
from nose.tools import *

from datetime import timedelta
from remember import db
from remember.memento import Memento

def save(m):
    db.session.add(m)
    db.session.commit()

class TestMemento(TestCase):

    def test_new_memento_unqueued(self):
        m = Memento("new")
        save(m)
        assert_equal(Memento.queue(), [])

    def test_hour_old_memento_queued(self):
        m = Memento("new")
        save(m)
        m.created_at -= timedelta(0, 3600) # one hour ago
        save(m)
        assert_equal(len(Memento.queue()), 1)

        qi = Memento.queue()[0]

        assert_equal(qi.threshold.name, 'hour')
        assert_equal(qi.memento, m)

    def test_week_old_memento_queued(self):
        m = Memento("new")
        save(m)
        m.created_at -= timedelta(7) # one week ago
        save(m)
        assert_equal(len(Memento.queue()), 3)

        qi_hour, qi_day, qi_week = Memento.queue()

        assert_equal(qi_hour.threshold.name, 'hour')
        assert_equal(qi_hour.memento, m)

        assert_equal(qi_day.threshold.name, 'day')
        assert_equal(qi_day.memento, m)

        assert_equal(qi_week.threshold.name, 'week')
        assert_equal(qi_week.memento, m)


