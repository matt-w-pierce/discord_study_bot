import requests, json
from random import choice
from datetime import datetime
from .. import scheduler, db
from ..models import Question


@scheduler.task(trigger='interval', id='do_post_question', seconds=30)
def post_question():
    with scheduler.app.app_context():

        # Getting the 20 questions that we asked the least recently
        q_query = Question.query.order_by(Question.last_asked).limit(20).all()
        questions = [q.to_dict() for q in q_query]

        # Randomly picking a question from this list to be displayed
        q = choice(questions)

        # Posting the question to Discord
        hook_url = 'https://discordapp.com/api/webhooks/702270009887555657/mytFno51Sq4fx0wvKyr22S8EwpSOFmLxyEUasKLoOnGoKurhWduq7uqRDpHBlNtMtL1C'
        msg_txt = f'_ _\n**Subject: **{q["set_name"]}\n**Question:**\n{q["prompt"]}\n\n**Answer:**\n||{q["answer"]}||\n_ _'
        data = {
            'content': msg_txt
        }
        result = requests.post(hook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))

            # Updating the last_asked value for this question and writing to database
            q_row = Question.query.get(q['id'])
            q_row.last_asked = datetime.now()
            db.session.add(q_row)
            db.session.commit()
