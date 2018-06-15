import os
from pymongo import MongoClient

class MissingDBConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)

class DBFactory(object):
    @staticmethod
    def create():
        try:
            db_host = os.environ['DB_HOST']
            db_port = int(os.environ['DB_PORT'])
            db_name = os.environ['DB_NAME']

            return MongoClient(db_host, db_port)[db_name]
        except KeyError as e:
            raise MissingDBConfigError('Missing {} environment variable'.format(str(e)))
