def find_country(country):
    """Возвращает индекс словаря содержащего искомую страну """
    try:
        for i in stations_json['countries']:
            if i['title'] == country:
                temp1 = stations_json['countries'].index(i)
            else:
                pass
    except:
            pass
    try:
        for i in stations_json['countries'][temp1]['regions']:
            if i['title'] == region:
                temp2 = stations_json['countries'][temp1]['regions'].index(i)
            else:
                pass
    except:
        pass
    try:
        for i in stations_json['countries'][temp1]['regions'][temp2]['settlements']:
            if i['title'] == city:
                temp3 = stations_json['countries'][temp1]['regions'][temp2]['settlements'].index(i)
            return stations_json['countries'][temp1]['regions'][temp2]['settlements'][temp3]['codes']['yandex_code']
        else:
            pass
    except:
        pass




def find_region(country, region):
    """Возвращает индекс словаря содержащего искомый регион"""
    temp = find_country(country)
    for i in stations_json['countries'][temp]['regions']:
        if i['title'] == region:
            return stations_json['countries'][temp]['regions'].index(i)
        else:
            pass

def find_code(country, region, city):
    """Возвращает код города по кодификатору яндекс расписания"""
    temp1 = find_country(country)
    temp2 = find_region(country, region)
    for i in stations_json['countries'][temp1]['regions'][temp2]['settlements']:
        if i['title'] == city:
            temp3 = stations_json['countries'][temp1]['regions'][temp2]['settlements'].index(i)
            return stations_json['countries'][temp1]['regions'][temp2]['settlements'][temp3]['codes']['yandex_code']
        else:
            pass




def parsing_api(request: dict):
    prt = ""
    count = 1
    try:
        for i in request['segments']:
            prt += f"{count}.\nВремя отправления: {i['arrival']}\nВремя прибытия: {i['departure']}\nВремя в пути: {float(i['duration'])/60}\nРейс: {i['thread']['title']}\nЦена билета: {float(i['tickets_info']['places'][0]['price']['whole'])+float(i['tickets_info']['places'][0]['price']['cents'])/100}\n\n"
            count += 1
    except:
        return None
    return prt