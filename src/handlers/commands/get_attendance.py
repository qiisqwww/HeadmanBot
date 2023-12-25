from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.dto.models import Student
from src.enums import Role, TelegramCommand
from src.kernel import Router
from src.resources import (
    CHOOSE_PAIR_TEMPLATE,
    NO_LESSONS_TODAY_TEMPLATE,
    WHICH_PAIR_TEMPLATE,
    choose_lesson_buttons,
    main_menu,
)
from src.services import LessonService

__all__ = [
    "get_stat_command_router",
]


get_stat_command_router = Router(
    must_be_registered=True,
    minimum_role=Role.VICE_HEADMAN,
)


@get_stat_command_router.message(F.text == TelegramCommand.GET_ATTENDANCE)
@logger.catch
async def getstat_command(message: Message, student: Student, lesson_service: LessonService) -> None:
    lessons = await lesson_service.filter_by_group_id(student.group_id)

    if not lessons:
        await message.answer(NO_LESSONS_TODAY_TEMPLATE)
        return

    await message.answer(CHOOSE_PAIR_TEMPLATE, reply_markup=main_menu(student.role))
    await message.answer(WHICH_PAIR_TEMPLATE, reply_markup=choose_lesson_buttons(lessons))
