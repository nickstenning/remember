from os import environ as env
import logging

DEFAULT_LOG_LEVEL = 'WARN'
DEFAULT_LOG_FORMAT = '[%(name)s] [%(levelname)s] %(message)s'

class ConfigError(Exception):
    pass


def configure(app):
    c = app.config

    app.debug   = _switch('DEBUG', False)
    app.testing = _switch('TESTING', False)

    # Optional settings
    c.setdefault('SQLALCHEMY_DATABASE_URI', env.get('DATABASE_URL',
                                                    'sqlite:///%s/remember.db' % app.instance_path))

    # Required settings
    c['SECRET_KEY']        = env['SECRET_KEY']
    c['CLOCKWORK_API_KEY'] = env['CLOCKWORK_API_KEY']
    c['CLOCKWORK_TO']      = env['CLOCKWORK_TO']
    c['CLOCKWORK_FROM']    = env['CLOCKWORK_FROM']


def configure_logging():
    log_level = env.get('APP_LOG_LEVEL', DEFAULT_LOG_LEVEL).upper()
    log_format = env.get('APP_LOG_FORMAT', DEFAULT_LOG_FORMAT)

    logging.basicConfig(format=log_format, level=getattr(logging, log_level))


def _switch(key, default=False):
    if key in env:
        return env[key].lower() != 'false'
    else:
        return default
