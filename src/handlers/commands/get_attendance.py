from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.kernel.resources.buttons import main_menu
from src.kernel.role import Role
from src.kernel.student_dto import StudentDTO
from src.modules.attendance.internal.resources.inline_buttons import (
    choose_lesson_buttons,
)
from src.modules.attendance.internal.resources.templates import (
    CHOOSE_PAIR_MESSAGE,
    NO_LESSONS_TODAY,
    WHICH_PAIR_MESSAGE,
)
from src.modules.attendance.internal.services import LessonService

__all__ = [
    "commands_router",
]


commands_router = Router(
    must_be_registered=True, minimum_role=Role.VICE_HEADMAN, services={"lesson_service": LessonService}
)


@commands_router.message(F.text == "Узнать посещаемость")
@logger.catch
async def getstat_command(message: Message, student: StudentDTO, lesson_service: LessonService) -> None:
    logger.trace("'/getstat' command started.")

    lessons = await lesson_service.filter_by_group_id(student.group_id)

    if not lessons:
        await message.answer(NO_LESSONS_TODAY)
        return

    await message.answer(CHOOSE_PAIR_MESSAGE, reply_markup=main_menu(student.role))
    await message.answer(WHICH_PAIR_MESSAGE, reply_markup=choose_lesson_buttons(lessons))
