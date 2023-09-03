import json

import requests

url = "https://geeks.kg/api/v1/courses/"

payload={}
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'ru',
  'Accept-Encoding': 'gzip, deflate, br'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
data = response.text
jsonify = json.loads(data)
print(jsonify['courses'])