import os


class Config:
    DEBUG = False
    FLASK_DEBUG = 0
    SECRET_KEY = "You can do this man"



class DevelopmentConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True



class TestConfig(Config):
    FLASK_DEBUG = 1
    DEBUG = True
  
configs = dict(
    test = TestConfig,
    production=Config,
    development=DevelopmentConfig
)