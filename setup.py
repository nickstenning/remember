from setuptools import setup, find_packages

setup(
    name = 'remember',
    version = '0.0.1',
    packages = find_packages(),

    install_requires = [
        'Flask==0.9',
        'Flask-SQLAlchemy==0.16',
    ],
)
