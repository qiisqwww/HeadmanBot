from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.resources import main_menu
from src.enums import Role
from src.dto import Student
from src.resources import choose_lesson_buttons
from src.resources import (
    CHOOSE_PAIR_MESSAGE,
    NO_LESSONS_TODAY,
    WHICH_PAIR_MESSAGE,
)
from src.services import LessonService

__all__ = [
    "commands_router",
]


commands_router = Router(
    must_be_registered=True, minimum_role=Role.VICE_HEADMAN, services={"lesson_service": LessonService}
)


@commands_router.message(F.text == "Узнать посещаемость")
@logger.catch
async def getstat_command(message: Message, student: Student, lesson_service: LessonService) -> None:
    logger.trace("'/getstat' command started.")

    lessons = await lesson_service.filter_by_group_id(student.group_id)

    if not lessons:
        await message.answer(NO_LESSONS_TODAY)
        return

    await message.answer(CHOOSE_PAIR_MESSAGE, reply_markup=main_menu(student.role))
    await message.answer(WHICH_PAIR_MESSAGE, reply_markup=choose_lesson_buttons(lessons))
