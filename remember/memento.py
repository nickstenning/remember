from collections import namedtuple
from datetime import datetime
from remember import db
from remember import thresholds

__all__ = ['Memento']

class Memento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    hour   = db.Column(db.Boolean, default=False)
    day    = db.Column(db.Boolean, default=False)
    week   = db.Column(db.Boolean, default=False)
    month  = db.Column(db.Boolean, default=False)
    month3 = db.Column(db.Boolean, default=False)
    month6 = db.Column(db.Boolean, default=False)
    year   = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        return '<Memento %r>' % self.id

    @classmethod
    def queue(cls):
        q = []

        for t in thresholds.THRESHOLDS:
            unprocessed = getattr(Memento, t.name) == False
            passed_threshold = Memento.created_at < datetime.utcnow() - t.delta
            for m in Memento.query.filter(unprocessed, passed_threshold).all():
                q.append(QueueItem(t, m))

        return q


QueueItem = namedtuple('QueueItem', 'threshold memento')
