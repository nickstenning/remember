from logging import getLogger

from flask import current_app

from remember import db
from remember.clockwork import Clockwork
from remember.memento import Memento

log = getLogger(__name__)

def send_pending():
    sms   = Clockwork(current_app.config['CLOCKWORK_API_KEY'])
    to    = current_app.config['CLOCKWORK_TO']
    from_ = current_app.config['CLOCKWORK_FROM']

    for item in Memento.queue():
        time = item.threshold.desc
        text = item.memento.text
        msg = '{0} ago: {1}'.format(time, text)

        log.info('Sending "{0}"'.format(msg))
        res = sms.send(to, msg, from_=from_)

        if not res.ok:
            for err in res.errors:
                log.error('Clockwork error: %s', err)
        else:
            setattr(item.memento, item.threshold.name, True)
            db.session.commit()
