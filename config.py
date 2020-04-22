import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'
    FLASKY_ADMIN = 'matt.pierce5695@gmail.com'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(application):
        pass


class DevelopmentConfig(Config):
    # Setting debug to True for development
    DEBUG = True

    # Below is what the URI should be when I have a local database setup
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Mustangs18!@127.0.0.1/discord_bot'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
