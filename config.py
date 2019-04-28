import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    MAIL_PORT = 2525
    MAIL_USE_TLS = False
    MAIL_SERVER = "smtp.mailtrap.io"
    MAIL_USERNAME = "27784b00f2e7e28ac"
    MAIL_PASSWORD = "d3b33d3d362c6c"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URL = "localhost"


class TestingConfig(Config):
    TESTING = True
