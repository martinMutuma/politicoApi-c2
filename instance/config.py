import os


class Config:
    DEBUG = False
    FLASK_DEBUG = 0
    SECRET_KEY = "You can do this man"
    CONNECTION_STRING = "dbname='political' user='postgres' host='localhost' password='admin' port='5432'"



class DevelopmentConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True



class TestConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    CONNECTION_STRING = "dbname='political_test' user='postgres' host='localhost' password='admin' port='5432'"
  
configs = dict(
    testing = TestConfig,
    production=Config,
    development=DevelopmentConfig
)