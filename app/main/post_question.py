import requests, json
from random import choice
from datetime import datetime
from .. import scheduler, db
from ..models import Question

test_url = 'https://discordapp.com/api/webhooks/702270009887555657/mytFno51Sq4fx0wvKyr22S8EwpSOFmLxyEUasKLoOnGoKurhWduq7uqRDpHBlNtMtL1C'
ap_url = 'https://discordapp.com/api/webhooks/702887067625062451/ERkWP2WnZ9VHrXvi0jwyDQIMur_5teoU4kVESBh863wGffsDeQMc0Sqf2sw8mixFsrmm'
pharm_url = 'https://discordapp.com/api/webhooks/703048422231375903/Q3dq_CWinB7KGGbCI9fNRtw6S2VNDqf404gebUQVv4Idw_M60kRTq-1hzhGMQs5n3OYN'


# @scheduler.task(trigger='cron', id='post_ap_hour', hour='8-20/2')
@scheduler.task(trigger='cron', id='post_ap_halfhour', minute='*/1', args=['Anesthesia Principles I', ap_url])
@scheduler.task(trigger='cron', id='post_pharm_halfhour', minute='*/1', args=['Nagelhout Pharmacology II', pharm_url])
def post_question(set_name, hook_url):
    with scheduler.app.app_context():

        # Getting the 20 questions that we asked the least recently
        q_query = Question.query.filter(Question.set_name == set_name).order_by(Question.last_asked).limit(20).all()
        questions = [q.to_dict() for q in q_query]

        # Randomly picking a question from this list to be displayed
        q = choice(questions)

        # Formatting message and sending
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
