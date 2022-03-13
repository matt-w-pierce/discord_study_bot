import os

import requests
import json
from random import choice, choices
from datetime import datetime
from .. import scheduler, db
from ..models import Question

test_url = os.getenv('test_url')
unit_1_url = os.getenv('unit_1_url')
unit_2_url = os.getenv('unit_2_url')
unit_3_url = os.getenv('unit_3_url')
unit_4_url = os.getenv('unit_4_url')
unit_5_url = os.getenv('unit_5_url')
unit_6_url = os.getenv('unit_6_url')
unit_7_url = os.getenv('unit_7_url')
unit_8_url = os.getenv('unit_8_url')
unit_9_url = os.getenv('unit_9_url')
unit_10_url = os.getenv('unit_10_url')
unit_11_url = os.getenv('unit_11_url')
unit_12_url = os.getenv('unit_12_url')


@scheduler.task(trigger='cron', id='unit_1', hour='8-20/2', args=[['Airway Anatomy', 'Respiratory Physiology', 'Airway Management'], None, unit_1_url])
@scheduler.task(trigger='cron', id='unit_2', hour='8-20/2', args=[['ANS'], None, unit_2_url])
@scheduler.task(trigger='cron', id='unit_3', hour='8-20/2', args=[['Cardiac A&P', 'Valvular Heart Disease', 'Cardiac Patho'], None, unit_3_url])
@scheduler.task(trigger='cron', id='unit_4', hour='8-20/2', args=[['Pharmacokinetics', 'Pharmacodynamics', 'IV Anesthetics', 'Volatile Anesthetics I', 'Volatile Anesthetics II'], None, unit_4_url])
@scheduler.task(trigger='cron', id='unit_5', hour='8-20/2', args=[['Local Anesthetics', 'Neuromuscular Blockers', 'NMBD Reversal', 'Opioid Agonists and Antagonists'], None, unit_5_url])
@scheduler.task(trigger='cron', id='unit_6', hour='8-20/2', args=[['AGM', 'Breathing Circuit', 'Monitoring I (Respiratory)', 'Monitoring II (HD)', 'Monitoring III (CV)', 'Monitoring IV (Misc)'], None, unit_6_url])
@scheduler.task(trigger='cron', id='unit_7', hour='8-20/2', args=[['Brain', 'Spine', 'Musculoskeletal'], None, unit_7_url])
@scheduler.task(trigger='cron', id='unit_8', hour='8-20/2', args=[['Neuraxial Anesthesia', 'Upper Extremity RA', 'Lower Extremity RA'], None, unit_8_url])
@scheduler.task(trigger='cron', id='unit_9', hour='8-20/2', args=[['Fluids and Electrolytes', 'Coagulation', 'Transfusion'], None, unit_9_url])
@scheduler.task(trigger='cron', id='unit_10', hour='8-20/2', args=[['Liver', 'Kidney', 'Endocrine'], None, unit_10_url])
@scheduler.task(trigger='cron', id='unit_11', hour='8-20/2', args=[['Obstetrics', 'Pediatrics', 'Geriatrics', 'Neonate I', 'Neonate II', 'Neonate III'], None, unit_11_url])
@scheduler.task(trigger='cron', id='unit_12', hour='8-20/2', args=[['Chemistry and Physics', 'Miscellaneous I', 'Miscellaneous II', 'Obesity', 'Positioning and Nerve Injuries', 'Professional Issues'], None, unit_12_url])
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
