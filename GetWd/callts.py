import requests, json
import datetime

webhook_url  = 'hogehoge'

dt_now = datetime.datetime.now()
date = dt_now.strftime('<@&hoge>')
text = date
main_content = {'content': text}
headers      = {'Content-Type': 'application/json'}

response     = requests.post(webhook_url, json.dumps(main_content), headers=headers)
