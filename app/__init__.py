from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from config import config

scheduler = APScheduler()
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()


# Creating the actual application
def create_app(config_name):
    application = Flask(__name__)

    application.config.from_object(config[config_name])
    config[config_name].init_app(application)

    bootstrap.init_app(application)
    moment.init_app(application)
    db.init_app(application)

    scheduler.init_app(application)
    scheduler.start()

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    return application
