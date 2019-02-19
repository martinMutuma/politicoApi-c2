import os


class Config:
    os.environ["FLASK_ENV"] = 'production'

    DEBUG = False
    FLASK_DEBUG = 0
    SECRET_KEY = "You can do this man"
    JWT_ALGORITHM = 'HS256'
    CONNECTION_STRING = os.environ["CONNECTION_STRING"]


class DevelopmentConfig(Config):
    os.environ["FLASK_ENV"] = 'development'

    FLASK_DEBUG = 1
    DEBUG = True


class TestConfig(Config):
    os.environ["FLASK_ENV"] = 'testing'
    FLASK_DEBUG = 1
    DEBUG = True
    TESTING = True
    CONNECTION_STRING = os.environ["CONNECTION_STRING"]


configs = dict(
    testing=TestConfig,
    production=Config,
    development=DevelopmentConfig
)
default_admin = dict(firstname='Admin', lastname="Default",
                     email='admin@mail.com', password='password', isAdmin=True,
                     passporturlstring='www.urladmon.com')
