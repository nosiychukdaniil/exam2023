import requests
import pprint
TOKEN = '4f28fc61-db4e-43cf-9520-38fcdbe4f93c'
USER_AGENT = 'Directory Sync Example'

headers = {
        'Authorization': 'OAuth ' + TOKEN,
        'User-Agent': USER_AGENT,
    }

response = requests.get('https://api.weather.yandex.ru/v2/informers?lat=55.75396&lon=37.620393', headers=headers)
# response.raise_for_status()
response_data = response.json()
result = response_data
pprint(result)