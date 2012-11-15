from os import environ as env
import urlparse

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
    c['SECRET_KEY'] = env['SECRET_KEY']

def _switch(key, default=False):
    if key in env:
        return env[key].lower() != 'false'
    else:
        return default
