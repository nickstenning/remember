from os import environ as env
import nose

if __name__ == '__main__':

    env.update({
        'TESTING': 'True',
        'DATABASE_URL': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-random-secret-key',
    })

    nose.main()
