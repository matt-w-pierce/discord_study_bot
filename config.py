import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'
    FLASKY_ADMIN = 'matt.pierce5695@gmail.com'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'matt.pierce5695@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'wiefizpkxwwmsvmb')
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
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Mustangs18!@127.0.0.1/discord_bot'


class ProductionConfig(Config):
    # Setting debug to false
    DEBUG = False

    # Below is what the URI should be when I have a local database setup
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Mustangs18!@127.0.0.1/discord_bot'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
