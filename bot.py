# Испортируем все необходимые модули
import logging, json, requests, os
from main import find_code, find_country, find_region, parsing_api
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
BOT_TOKEN = '5721867505:AAHHQh8KdLuaAKQhqasx_FyeHA-TRDHsvAI'
YANDEX_TOKEN = 'ace58ce6-ffcb-4755-ba76-bcd5b3b4ba57'
URL = 'https://api.rasp.yandex.net/v3.0/search/?'
URL_COPYRIGHT = 'https://api.rasp.yandex.net/v3.0/copyright/?'
URL_STATIONS_LIST = 'https://api.rasp.yandex.net/v3.0/stations_list/?'
MESS_MAX_LENGTH = 4096


param2 = {
    'apikey': YANDEX_TOKEN
}

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

#Определяем класс состояний конечного автомата FSM и сами состояния, все свойства класса наследуются от суперкласса StatesGroup
class FSM(StatesGroup):
    date_state = State()
    from_country_state = State()
    from_region_state = State()
    from_city_state = State()
    to_country_state = State()
    to_region_state = State()
    to_city_state = State()
    transport_type_state = State()



plane = KeyboardButton('самолет')
train = KeyboardButton('поезд')
suburban = KeyboardButton('электричка')
bus = KeyboardButton('автобус')
water = KeyboardButton('морской транспорт')
helicopter = KeyboardButton('вертолет')
dict_transport_types = {'самолет':'plane','поезд':'train','электричка':'suburban','автобус':'bus','морской транспорт':'water','вертолет':'helicopter'}
kb_transport_types = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_transport_types.row(bus,train, suburban).row(plane,helicopter)


russia = KeyboardButton('Россия')
ak = KeyboardButton('Алтайский край')
kb_russia = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(russia)
kb_ak = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(ak)
copyright_request = requests.get(URL_COPYRIGHT, params=param2)
copyright_text = copyright_request.json()['copyright']['text']
copyright_url = copyright_request.json()['copyright']['url']
stations_json = requests.get(URL_STATIONS_LIST, params=param2).json()


def find_code(country, region, city):
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


def parsing_api(request: dict):
    prt = ""
    count = 1
    try:
        for i in request['segments']:
            prt += f"{count}.\nВремя отправления: {i['arrival']}\nВремя прибытия: {i['departure']}\nВремя в пути: {float(i['duration'])/60/60} ч.\nРейс: {i['thread']['title']}\nЦена билета: {float(i['tickets_info']['places'][0]['price']['whole'])+float(i['tickets_info']['places'][0]['price']['cents'])/100}\n\n"
            count += 1
    except:
        return None
    return prt


#   Отправляет сообщение при отправке команд start или help
@dp.message_handler(commands=['start'], state=None)
async def process_start_command(message: types.Message):
    await FSM.date_state.set()
    await message.reply(f'Здравствуйте, с помощью данного бота вы можете узнать расписание транспорта между интерисующими вас населенными пунктами\n\nЧтобы продолжить работу введите дату планируемой поездки в формате ГГГГ-ММ-ДД\n\n{copyright_text}\n{copyright_url}')

@dp.message_handler(state=FSM.date_state)
async def print_date(message : types.Message, state : FSM):
    async with state.proxy() as data:
        data['date'] = message.text
    await FSM.next()
    await message.reply("Введите страну отправления:", reply_markup=kb_russia)

@dp.message_handler(state=FSM.from_country_state)
async def print_from_country(message : types.Message, state : FSM):
    async with state.proxy() as data:
        data['from_country'] = message.text
    await FSM.next()
    await message.reply("Введите регион отправления:", reply_markup=kb_ak)

@dp.message_handler(state=FSM.from_region_state)
async def print_from_region(message : types.Message, state : FSM):
    async with state.proxy() as data:
        data['from_region'] = message.text
    await FSM.next()
    await message.reply("Введите город отправления:")

@dp.message_handler(state=FSM.from_city_state)
async def print_from_city(message : types.Message, state : FSM):
    async with state.proxy() as data:
        data['from_city'] = message.text
    await FSM.next()
    await message.reply("Введите страну назначения:",reply_markup=kb_russia)

@dp.message_handler(state=FSM.to_country_state)
async def print_to_country(message : types.Message, state : FSM):
    async with state.proxy() as data:
        data['to_country'] = message.text
    await FSM.next()
    await message.reply("Введите регион назначения:", reply_markup=kb_ak)

@dp.message_handler(state=FSM.to_region_state)
async def print_to_region(message : types.Message, state : FSM):
    async with state.proxy() as data:
        data['to_region'] = message.text
    await FSM.next()
    await message.reply("Введите город назначения:")

@dp.message_handler(state=FSM.to_city_state)
async def print_to_city(message : types.Message, state : FSM):
    async with state.proxy() as data:
        data['to_city'] = message.text
    await FSM.next()
    await message.reply("Введите вид транспорта на котором вы хотите отправиться:", reply_markup=kb_transport_types)

@dp.message_handler(state=FSM.transport_type_state)
async def print_to_city(message : types.Message, state : FSM):
    try:
        async with state.proxy() as data:
            data['transport_type'] = message.text
            params = {
                'apikey': YANDEX_TOKEN,       #   Токен API
                'transport_types': dict_transport_types[data['transport_type']],                             #   Тип транспорта
                'from': find_code(data['from_country'], data['from_region'],data['from_city']), #   Откуда
                'to': find_code(data['to_country'], data['to_region'],data['to_city']),  #   Куда
                'format': 'json',                                       #   Формат данных получаемых от API
                'lang': 'ru_RU',                                        #   Язык данных от API
                'date': data['date']
            }
            rasp_api = requests.get(URL, params=params).json()
            if parsing_api(rasp_api) != None:
                for x in range(0, len(parsing_api(rasp_api)), MESS_MAX_LENGTH):
                            mess = parsing_api(rasp_api)[x: x + MESS_MAX_LENGTH]
                            await message.reply(mess)
            else:
                await message.reply("Ничего нет")
            await state.finish()
    except:
        await message.reply('Попробуйте еще раз \n/start')
        await state.finish()
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)