import requests, json
from random import choice, choices
from datetime import datetime
from .. import scheduler, db
from ..models import Question

test_url = 'https://discordapp.com/api/webhooks/702270009887555657/mytFno51Sq4fx0wvKyr22S8EwpSOFmLxyEUasKLoOnGoKurhWduq7uqRDpHBlNtMtL1C'
unit_1_url = 'https://discord.com/api/webhooks/904471895410360321/IiQ49M-uSKktqu33W5SrRARcu8AZR7Usd4pVjdIX4sGNKW17TKF_nTnSIJN2LRdpva5x'
unit_2_url = 'https://discord.com/api/webhooks/904472615740129290/3QeLZC8lOfeyioNQFhuZXo5XgIL3tpmZNnqVhtU2HeE-_VVYEJ4GYcXNLhjXgMymBzWk'
unit_3_url = 'https://discord.com/api/webhooks/904472942744834148/lsw253GREGR2Qug0tHNF2XYpida-6XdOHJUe5pt3QbROopfNho73_DMXbSUj6qkm6M8P'
unit_4_url = 'https://discord.com/api/webhooks/904473171506364458/nYFgwVpcNh2LZ9Dz4aBwTJIldrP4AiL3izOkhqf6SKWvswZqq3hRFuDWvRXMAArASGhO'
unit_5_url = 'https://discord.com/api/webhooks/904473813524295720/mrAlmUSzwGTi1KgCv0sZ34rvrFZy34eQd-erWYM8UKSwBmwwugc2wnYJaTPVjpWvsZEF'
unit_6_url = 'https://discord.com/api/webhooks/904473885771182140/1Fe77feGiaV16Joiu6mzXyvpOdP3yjLLKTE03xXVbqoJvamF18ReAzdM1piBsBNPCzIA'
unit_7_url = 'https://discord.com/api/webhooks/904473967199387680/ewK30TDffuOGGr2WnAWMKMqdmhy-v1jxe1QtABDONdGPS-U6DWfk3_Ud9g4MxgSuJkEV'
unit_8_url = 'https://discord.com/api/webhooks/904474047432245298/dZ1LUn1l4RAKqA4VoxeOHjwkHouCXnOcdtCXjk6XBRJ19skeSv1FJAcnL9S_m2rFxJOP'
unit_9_url = 'https://discord.com/api/webhooks/904474123097481268/_MVE8F8RiSkVDkn-EZT42FEsarugBc3jk4BYMD5pyA5kCuyfaFI71N53mvWqqRD5EZNW'
unit_10_url = 'https://discord.com/api/webhooks/904474198645293086/0IZaH3_S52fBidxo2fV4ZzUE_uqgcTQtKZ0NkeJI0W3urjhuT-fo97uZGpL9SOEY8U4_'
unit_11_url = 'https://discord.com/api/webhooks/904474270304960564/GI7_8uOQXrZqayCOPzf-sMsTMxXtIozF8bKCypbe2M-t-t61eleEQA5J1GICUdYEehtV'
unit_12_url = 'https://discord.com/api/webhooks/904474343713697812/G4NrLfhWbJCp4xEm5K4H_inxTqgVTt8qjqnnSYkVIeC53cJujR0HYhpDhY3LiK23qiUi'

@scheduler.task(trigger='cron', id='unit_1', hour='8-20/2', args=[['Airway Anatomy', 'Respiratory Physiology', 'Airway Management'], None, unit_1_url])
@scheduler.task(trigger='cron', id='unit_2', hour='8-20/2', args=[['ANS'], None, unit_2_url])
@scheduler.task(trigger='cron', id='unit_3', hour='8-20/2', args=[['Cardiac A&P', 'Valvular Heart Disease', 'Cardiac Patho'], None, unit_3_url])
@scheduler.task(trigger='cron', id='unit_4', hour='8-20/2', args=[['Pharmacokinetics', 'Pharmacodynamics', 'IV Anesthetics', 'Volatile Anesthetics I', 'Volatile Anesthetics II'], None, unit_4_url])
@scheduler.task(trigger='cron', id='unit_5', hour='8-20/2', args=[['Local Anesthetics', 'Neuromuscular Blockers', 'NMBD Reversal', 'Opioid Agonists and Antagonists'], None, unit_5_url])
@scheduler.task(trigger='cron', id='unit_6', hour='8-20/2', args=[['AGM', 'Breathing Circuit', 'Monitoring I (Respiratory)', 'Monitoring II (HD)', 'Monitoring III (CV)', 'Monitoring IV (Misc)'], None, unit_6_url])
@scheduler.task(trigger='cron', id='unit_7', hour='8-20/2', args=[['Brain', 'Spine', 'Musculoskeletal'], None, unit_7_url])
@scheduler.task(trigger='cron', id='unit_8', hour='8-20/2', args=[['Neuraxial Anesthesia', 'Upper Extremity RA', 'Lower Extremity RA'], None, unit_8_url])
@scheduler.task(trigger='cron', id='unit_9', hour='8-20/2', args=[['Fluids and Electrolytes', 'Coagulation', 'Transfusion'], None, unit_9_url])
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
