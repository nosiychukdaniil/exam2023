import json, requests, pprint

YANDEX_TOKEN = 'ace58ce6-ffcb-4755-ba76-bcd5b3b4ba57'
param2 = {
    'apikey': YANDEX_TOKEN
}  
# API URL
url = 'https://api.rasp.yandex.net/v3.0/search/?'
url2 = 'https://api.rasp.yandex.net/v3.0/stations_list/?'
list_st = requests.get(url2, params=param2)
data = list_st.json()


#Поиск в json
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

def parsing_api(request: dict):
    prt = ""
    count = 1
    for i in request['segments']:
        prt += f"{count}.\nВремя отправления: {i['arrival']}\nВремя прибытия: {i['departure']}\nВремя в пути: {float(i['duration'])/60}\nРейс: {i['thread']['title']}\nЦена билета: {float(i['tickets_info']['places'][0]['price']['whole'])+float(i['tickets_info']['places'][0]['price']['cents'])/100}\n\n"
        count += 1
    return prt