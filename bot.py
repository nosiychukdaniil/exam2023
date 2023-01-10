import json, requests, pprint
with open('list_st.json') as f:
    data = json.load(f)
print(type(data))


#Поиск в списке словарей
def find_country(text):
    for i in data['countries']:
        if i['title'] == text:
            return data['countries'].index(i)
        else:
            pass
def find_region(country, region):
    temp = find_country(country)
    for i in data['countries'][temp]['regions']:
        if i['title'] == region:
            return data['countries'][temp]['regions'].index(i)
        else:
            pass
def find_code(country, region, city):
    temp1 = find_country(country)
    temp2 = find_region(country, region)
    for i in data['countries'][temp1]['regions'][temp2]['settlements']:
        if i['title'] == city:
            temp3 = data['countries'][temp1]['regions'][temp2]['settlements'].index(i)
            return data['countries'][temp1]['regions'][temp2]['settlements'][temp3]['codes']['yandex_code']
        else:
            pass

param = {
    'apikey': 'ace58ce6-ffcb-4755-ba76-bcd5b3b4ba57',
    'transport_types': 'train',
    'from': find_code("Россия", 'Алтайский край','Алейск'),
    'to': find_code("Россия", 'Алтайский край','Барнаул'),
    'format': 'json',
    'lang': 'ru_RU',
    'date': '2023-01-12'
    }
url = 'https://api.rasp.yandex.net/v3.0/search/?'