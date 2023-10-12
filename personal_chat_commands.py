#import logging
import random
from typing import Optional

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from config.config_reader import config
from work_api import API
from service import UsersService
from states import RegStates, SetHeadMen
from messages import (START_MESSAGE, REG_MESSAGE_1, REG_MESSAGE_2,
                      SUCCESFULLY_REG_MESSAGE, UNSUCCESFULLY_REG_MESSAGE, PASS_ASK_MESSAGE,
                      STAROSTA_REG_MESSAGE, UNSUCCESFULL_STAROSTA_REG_MESSAGE)
from middlewares import RegMiddleware

router = Router()
api = API()
list_pars = {'ind':'0'}
list_group = {}
router.message.middleware(RegMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

@router.message(Command("start"))
async def start_cmd(message: types.Message, state:FSMContext) -> None:
    await message.answer(text = START_MESSAGE + '\n'+ REG_MESSAGE_1)
    logging.info("start command")

    await state.set_state(RegStates.surname_input)

@router.message(RegStates.surname_input, F.text)
async def handling_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name_surname = message.text)
    logging.info("name and surname handled")

    await message.answer(text = REG_MESSAGE_2)

    await state.set_state(RegStates.group_input)

@router.message(RegStates.group_input, F.text)
async def handling_group(message: types.Message, state: FSMContext) -> None:
    await state.update_data(group = message.text)
    logging.info("group name handled")

    user_data = await state.get_data()

    with UsersService() as con:
        isreg : bool = con.registration(message.from_user.id,message.from_user.username,user_data["name_surname"],
                                        user_data["group"])
        if isreg: await message.answer(text = SUCCESFULLY_REG_MESSAGE)
        else: await message.answer(text = UNSUCCESFULLY_REG_MESSAGE)

        await state.clear()

@router.message(Command("set_headmen"))
async def start_headmen(message: types.Message, state:FSMContext) -> None:
    await message.answer(text = PASS_ASK_MESSAGE)

    await state.set_state(RegStates.surname_input)

@router.message(SetHeadMen.get_password, F.text)
async def get_password(message: types.Message, state:FSMContext) -> None:
    if message.text == config.PASSWORD.get_secret_value():
        with UsersService() as con:
            isset = con.set_headmen()
            if isset: await message.answer(text = STAROSTA_REG_MESSAGE)
            else: await message.answer(text = UNSUCCESFULL_STAROSTA_REG_MESSAGE)

    await state.clear()

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


async def job(k, bot):# k он ругается, если уберёшь отлично
    global list_pars, list_group
    list_pars = {'ind': '0'}
    list_group = {}
    with UsersService() as con:
        groups = con.get_groups()
        print(groups)
        for group in groups:
            list_group[group] = {}
            api.regenerate(group[0])
            day = api.get_today()
            for lesson in day:
                list_group[group]['_'.join(map(str, lesson))] = {'Y' : [], 'N' : []}
                print(con.get_user_of_group(group[0]), group)
                for Id in con.get_user_of_group(group[0]):
                    await bot(Id[0], f'Привет, ты будешь на паре {lesson[0]}, которая начнётся в {lesson[1]}', reply_markup=get_keyboard(lesson))

@router.callback_query(F.data.split('_')[0] == "n")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    data, flag = clbck.data.split('_')[1:]
    name, time = list_pars[data].split('_')
    with UsersService as con:
        con.g
    await clbck.message.edit_text(f"Ок я поняла, на паре {name}, которая начнётся в {time}, ты "
                                  f"{'' if flag == '1' else 'не '}будешь.",
                                  reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[]))
