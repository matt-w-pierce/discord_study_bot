import os
from app import create_app, db
from app.models import Question
from flask_migrate import Migrate


application = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(application, db)


@application.shell_context_processor
def make_shell_context():
    return dict(db=db, Question=Question)
