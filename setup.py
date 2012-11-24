from setuptools import setup, find_packages

setup(
    name = 'remember',
    version = '0.0.2',
    packages = find_packages(),

    install_requires = [
        'Flask==0.9',
        'Flask-SQLAlchemy==0.16',
        'requests==0.14.2',
    ],
)
