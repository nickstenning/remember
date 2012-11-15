from logging import getLogger

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from remember.config import configure

log = getLogger(__name__)
db = SQLAlchemy()

def create_app():
    log.debug("Creating %s application", __name__)
    app = Flask(__name__)

    configure(app)

    # Configure database
    db.init_app(app)

    # Mount views
    from remember import main
    app.register_blueprint(main.main)

    log.debug("Successfully created %s application", __name__)
    return app

def create_db(app):
    from remember import memento
    with app.test_request_context():
        db.create_all()

def drop_db(app):
    from remember import memento
    with app.test_request_context():
        db.drop_all()

