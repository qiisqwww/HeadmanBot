import schedule
from aiogram import Dispatcher, types

from work_api import API
from service import UsersService

api = API()
dp = None



def get_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def job(k, bot):
    # print(111)
    with UsersService() as con:
        groups = con.get_groups()
        # print(groups)
        for group in groups:
            api.regenerate(group[0])
            day = api.get_today()
            for lesson in day:
                # print(con.get_user_of_group(group[0]), group)
                for Id in con.get_user_of_group(group[0]):
                    await bot(Id[0], 'текст' + str(lesson), reply_markup=get_keyboard())




def restart_schedule(bot):
    #print(99999)
    #global dp
    #dp = Dispatcher(bot)
    schedule.every().second.do(job, bot=bot)

