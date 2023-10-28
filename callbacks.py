import logging

from aiogram import types, Router, F
from aiogram.enums import ParseMode

from service import UsersService
from middlewares import CallbackMiddleware
from messages import (ALL_MESSAGE, NONE_MESSAGE, attendance_for_headmen_message)
from buttons import load_attendance_kb, load_void_kb, load_choose_lesson_kb
from work_api import API


__all__ = ["router"]


router = Router()
router.callback_query.middleware(CallbackMiddleware())
api = API()


@router.callback_query(F.data.startswith("attendance"), flags={"callback": "poll"})
async def check_in_callback(callback: types.CallbackQuery):
    logging.info("check_in callback handled")
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
        api.regenerate(group)
        lessons = api.get_today()

        lessons_in_states = con.get_lessons(callback.from_user.id)
        already_chosen_lessons_in_numbers = []

        for lesson in range(len(lessons)):
            if lessons[lesson] == data:
                chosen_lesson = lesson
                already_chosen_lessons_in_numbers.append(lesson)
            if lessons_in_states[lesson] == '1':
                already_chosen_lessons_in_numbers.append(lesson)

        for i in sorted(already_chosen_lessons_in_numbers, reverse=True):
            lessons.pop(i)

        info = 'lesson ' + str(chosen_lesson)
        con.change_attendance(callback.from_user.id, info)

        await callback.message.edit_text(f'Вы посетите пару {data[0]}, '
                                         f'которая начнётся в {data[1]}',
                                         reply_markup=load_attendance_kb(lessons))


@router.callback_query(flags={"callback": "attendance"})
async def attendance_send_callback(callback: types.CallbackQuery):
    logging.info("attendance callback handled")

    with UsersService() as con:
        group = con.get_group_of_id_tg(callback.from_user.id)
        api.regenerate(group)
        lessons = api.get_today()

        await callback.message.edit_text(text=f"{lessons[int(callback.data)][0]}, "
                                            f"{lessons[int(callback.data)][1]}\n\n"
                                              + attendance_for_headmen_message(callback),
                                         reply_markup=load_choose_lesson_kb(lessons),
                                         parse_mode=ParseMode.HTML)
