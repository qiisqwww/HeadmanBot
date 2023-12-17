from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.dto.models import Student
from src.enums import Role
from src.kernel import Router
from src.resources import (
    CHOOSE_PAIR_MESSAGE,
    NO_LESSONS_TODAY,
    WHICH_PAIR_MESSAGE,
    choose_lesson_buttons,
    main_menu,
)
from src.services import LessonService

__all__ = [
    "get_stat_command_router",
]


get_stat_command_router = Router(must_be_registered=True, minimum_role=Role.VICE_HEADMAN)


@get_stat_command_router.message(F.text == "Узнать посещаемость")
@logger.catch
async def getstat_command(message: Message, student: Student, lesson_service: LessonService) -> None:
    logger.trace("'/getstat' command started.")

    lessons = await lesson_service.filter_by_group_id(student.group_id)

    if not lessons:
        await message.answer(NO_LESSONS_TODAY)
        return

    await message.answer(CHOOSE_PAIR_MESSAGE, reply_markup=main_menu(student.role))
    await message.answer(WHICH_PAIR_MESSAGE, reply_markup=choose_lesson_buttons(lessons))
