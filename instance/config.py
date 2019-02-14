import os


class Config:
    os.environ["FLASK_ENV"] = 'production'

    DEBUG = False
    FLASK_DEBUG = 0
    SECRET_KEY = "You can do this man"
    # CONNECTION_STRING = "dbname='political' user='postgres' host='localhost' password='admin' port='5432'"
    CONNECTION_STRING = os.environ["CONNECTION_STRING"]


class DevelopmentConfig(Config):
    os.environ["FLASK_ENV"] = 'development'

    FLASK_DEBUG = 1
    DEBUG = True



class TestConfig(Config):
    os.environ["FLASK_ENV"] = 'testing'
    # os.environ["CONNECTION_STRING"] = 'testing' "dbname='political_test' user='postgres' host='localhost' password='admin' port='5432'"
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    CONNECTION_STRING = os.environ["CONNECTION_STRING"]
  
configs = dict(
    testing = TestConfig,
    production=Config,
    development=DevelopmentConfig
)