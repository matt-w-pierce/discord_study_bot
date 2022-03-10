import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hard to guess string')
    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN', 'username@me.com')

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'username@me.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'password')
    MAIL_SUBJECT_PREFIX = 'Sparky - '
    MAIL_SENDER = 'Sparky <sparky-bot@studyhelper.com>'
    ADMINS = ['matt.pierce5695@gmail.com']

    # SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(application):
        pass


class DevelopmentConfig(Config):
    # Setting debug to True for development
    DEBUG = True

    # Below is what the URI should be when I have a local database setup
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class ProductionConfig(Config):
    # Setting debug to false
    DEBUG = False

    # Below is what the URI should be when I have a local database setup
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
