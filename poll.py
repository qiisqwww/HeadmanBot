#import logging

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from buttons import load_void_kb, load_attendance_kb
from work_api import API
from service import UsersService
from states import ReqPars
from middlewares import HeadmenCommandsMiddleware


router = Router()

router.message.middleware(HeadmenCommandsMiddleware())
router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях

api = API()


async def job(k, bot):  # ругается, если убрать k
    with UsersService() as con:
        groups = con.get_groups()
        print(groups)
        for group in groups:
            api.regenerate(group[0])
            day = api.get_today()
            seen = set()
            seen_add = seen.add
            day = [x for x in day if not (str(x) in seen or seen_add(str(x)))]
            for Id in con.get_user_of_group(group[0]):
                con.change_attendance(Id[0], f'start {len(day)}')

                print(con.get_user_of_group(group[0]), group)
                await bot(Id[0], f'Привет, ты будешь на паре', reply_markup=load_attendance_kb(day))


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
        kb = [[types.KeyboardButton(text=f'{lesson + 1}) {lessons[lesson][0]} {lessons[lesson][1]}')] for lesson in range(len(lessons))]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text='На какую пару сегодняшнего дня ты хочешь узнать информацию?', reply_markup=keyboard)
    await state.set_state(ReqPars.group_input_req)


@router.message(ReqPars.group_input_req, F.text)
async def group_input_req(message: types.Message, state: FSMContext) -> None:
    await message.answer(text='Отлично', reply_markup=types.ReplyKeyboardMarkup(keyboard=[]))
    with UsersService() as con:
        # message.text
        para = int(message.text.split(') ')[0]) - 1
        group = con.get_group_of_id_tg(message.from_user.id)
        no_list = []
        none_list = []
        ok_list = []
        for ID in con.get_user_of_group(group):
            ID = ID[0]
            print(con.get_pars(ID))
            if len(con.get_pars(ID).replace('0', '')) == 0:
                none_list.append(ID)
                continue
            match con.get_pars(ID)[para]:
                case '0': # мне лень при нажатии на кнопку я приду на пару n обновлять всю
                    # бд тем, что я не приду, поэтому я встроил такую проверку, да пиздец,
                    # но я на семинаре по процедурке, у меня есть ещё пара дел
                    no_list.append(ID)
                case '1':
                    ok_list.append(ID)
                case '2':
                    no_list.append(ID)
        none_text = 'Не отметились:\n'
        for user in none_list:
            none_text += str(con.get_user_of_id_tg(user)[3]) + '\n'
        on_text = 'Придут:\n'
        for user in ok_list:
            on_text += str(con.get_user_of_id_tg(user)[3]) + '\n'
        no_text = 'Не придут:\n'
        for user in no_list:
            no_text += str(con.get_user_of_id_tg(user)[3]) + '\n'
        await message.answer(text=f'{on_text}')
        await message.answer(text=f'{no_text}')
        await message.answer(text=f'{none_text}', reply_markup=load_void_kb())
        await state.clear()
