import logging

from aiogram import types, Router, F

from service import UsersService
from middlewares import CallbackMiddleware
from messages import (ALL_MESSAGE, NONE_MESSAGE, SKIP1_MESSAGE, SKIP2_MESSAGE,
                      SKIP3_MESSAGE, SKIP4_MESSAGE)
from buttons import load_attendance_kb

router = Router()
router.callback_query.middleware(CallbackMiddleware())

@router.callback_query(F.data.startswith("attendance"))
async def poll_callback(callback: types.CallbackQuery):
    logging.info("attendance callback handled")
    callback_data = callback.data.split("_")[1]

    with UsersService() as con:
        con.change_attendance(callback.from_user.id, callback_data)

    #3 в load_attendance_kb необходимо будет заменить на параметр = количеству пар у студента
    if callback_data == "all":
        await callback.message.edit_text(ALL_MESSAGE, reply_markup=load_attendance_kb(3))
    elif callback_data == "none":
        await callback.message.edit_text(NONE_MESSAGE, reply_markup=load_attendance_kb(3))
    elif callback_data == "1":
        await callback.message.edit_text(SKIP1_MESSAGE, reply_markup=load_attendance_kb(3))
    elif callback_data == "2":
        await callback.message.edit_text(SKIP2_MESSAGE, reply_markup=load_attendance_kb(3))
    elif callback_data == "3":
        await callback.message.edit_text(SKIP3_MESSAGE, reply_markup=load_attendance_kb(3))
    elif callback_data == "4":
        await callback.message.edit_text(SKIP4_MESSAGE, reply_markup=load_attendance_kb(3))

