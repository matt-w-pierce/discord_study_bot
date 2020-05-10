import os
import logging

from config import config

from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

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

    if not application.debug:
        mail_handler = SMTPHandler(
            mailhost=(application.config['MAIL_SERVER'], application.config['MAIL_PORT']),
            fromaddr='no-reply@studyhelper.com',
            toaddrs=application.config['ADMINS'],
            subject='Sparky Application Error',
            credentials=(application.config['MAIL_USERNAME'], application.config['MAIL_PASSWORD']),
            secure=()
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
        application.logger.addHandler(mail_handler)

    if not application.debug:
        print(os.getcwd())
        logging.info('Setting up logging file')
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/sparky.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        application.logger.addHandler(file_handler)

        application.logger.setLevel(logging.INFO)
        application.logger.info('Sparky startup')

    scheduler.init_app(application)
    scheduler.start()

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)

    return application
