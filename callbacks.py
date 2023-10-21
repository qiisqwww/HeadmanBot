import logging

from aiogram import types, Router, F

from service import UsersService
from middlewares import CallbackMiddleware
from messages import (ALL_MESSAGE, NONE_MESSAGE, SKIP1_MESSAGE, SKIP2_MESSAGE,
                      SKIP3_MESSAGE, SKIP4_MESSAGE)
from buttons import load_attendance_kb, load_void_kb
from work_api import API

router = Router()
router.callback_query.middleware(CallbackMiddleware())

@router.callback_query(F.data.startswith("attendance"))
async def poll_callback(callback: types.CallbackQuery):
    logging.info("attendance callback handled")
    if callback.data == 'no':
        await callback.message.edit_text("Поздно, ищи старосту в реале, ты отмечен как не проголосовавший", reply_markup=load_void_kb())
        return
    callback_data = callback.data.split("_")[1]
    with UsersService() as con:
        if callback_data == "all":
            con.change_attendance(callback.from_user.id, callback_data + ' 0')
            await callback.message.edit_text(ALL_MESSAGE, reply_markup=load_void_kb())
            return
        elif callback_data == "none":
            con.change_attendance(callback.from_user.id, callback_data + ' 0')
            await callback.message.edit_text(NONE_MESSAGE, reply_markup=load_void_kb())
            return
        data = [str(i[1:-1]) for i in callback_data[1:-1].split(', ')]
        group = con.get_group_of_id_tg(callback.from_user.id)
        api = API()
        api.regenerate(group)
        day = api.get_today()
        z = con.get_pars(callback.from_user.id)
        a = []
        info = 0
        for lesson in range(len(day)):
            if day[lesson] == data:
                info = lesson
                a.append(lesson)
            if z[lesson] == '1':
                a.append(lesson)
        for i in sorted(a,reverse=True):
            day.pop(i)
        info = 'lesson ' + str(info)
        con.change_attendance(callback.from_user.id, info)
        #3 в load_attendance_kb необходимо будет заменить на параметр = количеству пар у студента

        await callback.message.edit_text(f'Вы поситите {callback_data} пару', reply_markup=load_attendance_kb(day))

