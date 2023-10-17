import logging

from aiogram import types, Router, F

from service import UsersService


router = Router()


@router.callback_query(F.data.startswith("attendance"))
async def poll_callback(callback: types.CallbackQuery):
    logging.info("attendance callback handled")
    callback_data = callback.data.split("_")[1]

    with UsersService() as con:
        con.change_attendance(callback.from_user.id, callback_data)

