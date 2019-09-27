import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://postgres:postgres@localhost:5433/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
