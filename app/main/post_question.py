import requests, json
from random import choice, choices
from datetime import datetime
from .. import scheduler, db
from ..models import Question

test_url = 'https://discordapp.com/api/webhooks/702270009887555657/mytFno51Sq4fx0wvKyr22S8EwpSOFmLxyEUasKLoOnGoKurhWduq7uqRDpHBlNtMtL1C'
ap_url = 'https://discordapp.com/api/webhooks/702887067625062451/ERkWP2WnZ9VHrXvi0jwyDQIMur_5teoU4kVESBh863wGffsDeQMc0Sqf2sw8mixFsrmm'
pharm_url = 'https://discordapp.com/api/webhooks/703048422231375903/Q3dq_CWinB7KGGbCI9fNRtw6S2VNDqf404gebUQVv4Idw_M60kRTq-1hzhGMQs5n3OYN'
anat_url = 'https://discord.com/api/webhooks/703048779632476240/tRHSEwV9B_BcopXa69-vImpzvVSavBLlvFNcHiO_S_2uRd2jalSOL0MHz2zFUMuYrZFt'


@scheduler.task(trigger='cron', id='post_ap_hour', hour='8-20/2', args=[['Anesthesia Principles I', 'NA2 Exam 1'], None, ap_url])
@scheduler.task(trigger='cron', id='post_pharm_hour', hour='8-20/2', args=[['Nagelhout Pharmacology II'], None, pharm_url])
@scheduler.task(trigger='cron', id='post_anat_hour', hour='8-20/2', args=[['Intro and Back Anatomy', 'Head and Neck'], [0.5, 0.5], anat_url])
def post_question(set_name_l, set_weights, hook_url):
    with scheduler.app.app_context():

        if set_weights is not None:
            # If set weights are supplied, then choose a topic based on the weights
            set_name = choices(population=set_name_l, weights=set_weights, k=1)
            print(set_name)

        else:
            # If weights are not provided, then just pick a set randomly
            set_name = choice(set_name_l)
            print(set_name)

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
            print(f"Question posted for {set_name} at {str(datetime.now())}")

            # Updating the last_asked value for this question and writing to database
            q_row = Question.query.get(q['id'])
            q_row.last_asked = datetime.now()
            db.session.add(q_row)
            db.session.commit()
