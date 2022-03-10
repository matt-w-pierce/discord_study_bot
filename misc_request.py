import json
import requests

print('Running the misc request file!')

test_url = 'https://discordapp.com/api/webhooks/702270009887555657/mytFno51Sq4fx0wvKyr22S8EwpSOFmLxyEUasKLoOnGoKurhWduq7uqRDpHBlNtMtL1C'
prod_gen_url = 'https://discordapp.com/api/webhooks/702904914958876722/I1XQtljBH76eWWNuxvVLU1JE5OvpmR2CiLbNc2-YnumTR6-_PvluRHc17g320oXIKjrd'

msg_txt = 'Hello! My name is Spark-Bot, but my friends call me Sparky. I am excited to be your virtual anesthesia study buddy. I hope my “Questions-of-the-Day” SPARK your interest. Really, this forum is a way to help you SPARKle & shine your way to board-certification. I try to post questions every 2 hours from 8am-8pm, but I made sure to turn the notifications off so that I don’t disrupt your beauty sleep (I know that you all need it desperately). Happy studying, my anesthesia superstars. I believe in you!'
data = {
    'content': msg_txt
}
result = requests.post(prod_gen_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))
