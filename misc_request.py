import requests, json

print('Running the misc request file!')

test_url = 'https://discordapp.com/api/webhooks/702270009887555657/mytFno51Sq4fx0wvKyr22S8EwpSOFmLxyEUasKLoOnGoKurhWduq7uqRDpHBlNtMtL1C'
prod_url = 'https://discordapp.com/api/webhooks/702887067625062451/ERkWP2WnZ9VHrXvi0jwyDQIMur_5teoU4kVESBh863wGffsDeQMc0Sqf2sw8mixFsrmm'


msg_txt = 'Hello! and welcome to Spark-Bot. My name is Sparky, and I will be your virtual study buddy as you prepare for nurse anesthesia boards. I hope my questions-of-the-day help you spark-le & shine your way to graduation. Happy Studying'
data = {
	'content': msg_txt
}
result = requests.post(prod_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

try:
	result.raise_for_status()
except requests.exceptions.HTTPError as err:
	print(err)
else:
	print("Payload delivered successfully, code {}.".format(result.status_code))
