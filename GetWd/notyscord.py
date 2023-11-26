import requests, json
import datetime

def sendm(message):
	webhook_url = 'hogehoge'

	dt_now = datetime.datetime.now()
	#date = dt_now.strftime('@here %Y年%m月%d日 %H:%M:%S')
	text = message
	main_content = {'content': text}
	headers      = {'Content-Type': 'application/json'}

	response     = requests.post(webhook_url, json.dumps(main_content), headers=headers)
