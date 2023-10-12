import schedule
from aiogram import Dispatcher

from work_api import API
from service import UsersService
from config.config_reader import config
import json
import requests

api = API()
dp = None


def threat():  # второй поток для рассылки
    while True:
        schedule.run_pending()
def SendMessage(id, text):
    print(id, text)
    zap = f'''https://api.telegram.org/bot{config.BOT_TOKEN.get_secret_value()}/sendMessage'''
    params = {'chat_id': id, 'text': text, "reply_markup": json.dumps({
        "inline_keyboard": [
            [
                {
                    "text": "Даааа",
                    "callback_data": 'para'
                },
                {
                    "text": "Неееее",
                    "callback_data": 'para'
                }
            ]]
    })}
    return requests.get(zap, params=params).json()

def job(bot):
    print(111)
    with UsersService() as con:
        groups = con.get_groups()
        for group in groups:
            api.regenerate(group[0])
            day = api.get_today()
            for lesson in day:
                print(con.get_user_of_group(group[0]), group)
                for Id in con.get_user_of_group(group[0]):
                    SendMessage(Id, 'текст' + str(lesson))

    return schedule.CancelJob


def restart_schedule(bot):
    #print(99999)
    #global dp
    #dp = Dispatcher(bot)
    schedule.every().second.do(job, bot=bot)

