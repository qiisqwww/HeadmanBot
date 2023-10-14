#import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from work_api import API
from service import UsersService
from states import ReqPars
from middlewares import HeadmenCommandsMiddleware


router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = API()
list_pars = {'ind':'0'}
list_group = {}

def get_keyboard(data):
    data = '_'.join(map(str, data))
    list_pars[list_pars['ind']] = data
    data = list_pars['ind']
    buttons = [
        [types.InlineKeyboardButton(text="Да", callback_data=str(f'n_{data}_1')),
         types.InlineKeyboardButton(text="Нет", callback_data=str(f'n_{data}_0'))]
    ]
    list_pars['ind'] = hex(int(list_pars['ind'], 16) + 1)[2:]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def job(k, bot):  # ругается, если убрать k
    global list_pars, list_group
    list_pars = {'ind': '0'}
    list_group = {}
    with UsersService() as con:
        groups = con.get_groups()
        print(groups)
        for group in groups:
            list_group[group[0]] = {}
            api.regenerate(group[0])
            day = api.get_today()
            for lesson in day:
                list_group[group[0]]['_'.join(map(str, lesson))] = {'Y' : [], 'N' : []}
                print(con.get_user_of_group(group[0]), group)
                for Id in con.get_user_of_group(group[0]):
                    await bot(Id[0], f'Привет, ты будешь на паре {lesson[0]}, которая начнётся в {lesson[1]}', reply_markup=get_keyboard(lesson))

@router.callback_query(F.data.split('_')[0] == "n")
async def input_text_prompt(clbck: CallbackQuery):
    data, flag = clbck.data.split('_')[1:]
    name, time = list_pars[data].split('_')
    with UsersService() as con:
        group = con.get_group_of_id_tg(clbck.from_user.id)
        print(group)
        list_group[group][name+'_'+time]['Y' if flag == '1' else 'N'].append(clbck.from_user.id)
    print(list_group)
    await clbck.message.edit_text(f"Ок я поняла, на паре {name}, которая начнётся в {time}, ты "
                                  f"{'' if flag == '1' else 'НЕ '}БУДЕШЬ.",
                                  reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[]))

@router.message(Command("next"))
async def next_(message: types.Message, state: FSMContext) -> None:
    print(8888)
    with UsersService() as con:
        group = con.get_group_of_id_tg(message.from_user.id)
        api.regenerate(group)
        lessons = api.get_today()
        print(lessons)
        if len(lessons) == 0:
            await message.answer(text='пар сегодня нет')
            return
        kb = [[types.KeyboardButton(text=lesson[0] + '/' + lesson[1])] for lesson in lessons]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text='На какую пару сегодняшнего дня ты хочешь узнать информацию?', reply_markup=keyboard)
    await state.set_state(ReqPars.group_input_req)


@router.message(ReqPars.group_input_req, F.text)
async def group_input_req(message: types.Message, state: FSMContext) -> None:
    await message.answer(text='Отлично', reply_markup=types.ReplyKeyboardMarkup(keyboard=[]))
    with UsersService() as con:
        # message.text
        para = message.text.replace('/', '_')
        group = con.get_group_of_id_tg(message.from_user.id)
        api.regenerate(group)
        lesson = api.get_today()
        if len(lesson) == 0:
            await message.answer(text='пар сегодня нет')
            return
        print(list_group)
        print(group, para)
        ok_list = list_group[group][para]['Y']
        # no_list = list_group[group][para]['N']
        none_list = [i[0] for i in con.get_user_of_group(group) if i[0] not in ok_list]
        on_text = 'Придут:\n'
        for user in ok_list:
            on_text += str(con.get_user_of_id_tg(user)[3]) + '\n'
        no_text = 'Не придут:\n'
        for user in none_list:
            no_text += str(con.get_user_of_id_tg(user)[3]) + '\n'
        await message.answer(text=f'{on_text}')
        await message.answer(text=f'{no_text}')
