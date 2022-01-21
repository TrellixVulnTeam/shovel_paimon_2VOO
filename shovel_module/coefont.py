import hmac
import requests
import hashlib
import json
from datetime import datetime, timezone

def generate(accesskey,access_secret,text,path):
  text = '初めまして。今日から新たに読み上げを担当させていただくミリアルと申します。よろしくお願いします。'
  date: str = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
  data: str = json.dumps({
    'coefont': 'c28adf78-d67d-4588-a9a5-970a76ca6b07',
    'text': text
  })
  signature = hmac.new(bytes(access_secret, 'utf-8'), (date+data).encode('utf-8'), hashlib.sha256).hexdigest()

  response = requests.post('https://api.coefont.cloud/v1/text2speech', data=data, headers={
    'Content-Type': 'application/json',
    'Authorization': accesskey,
    'X-Coefont-Date': date,
    'X-Coefont-Content': signature
  })

  if response.status_code == 200:
    with open(f'{path}.wav', 'wb') as f:
      f.write(response.content)
  else:
    print(response.json())
