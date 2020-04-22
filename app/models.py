from . import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    set_name = db.Column(db.String(128), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    last_asked = db.Column(db.DateTime, default=datetime.now())

    @staticmethod
    def from_dict(d):
        set_name = d['set_name']
        prompt = d['prompt']
        answer = d['answer']
        new_q = Question(set_name=set_name, prompt=prompt, answer=answer, last_asked=datetime.now())
        return new_q

    def to_dict(self):
        d = {
            'id': self.id,
            'set_name': self.set_name,
            'prompt': self.prompt,
            'answer': self.answer,
            'last_asked': self.last_asked
        }
        return d
