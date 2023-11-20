from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types.message import Message
from asyncpg import Pool
from loguru import logger

from src.buttons import (choose_lesson_buttons,
                         default_buttons, )
from src.dto import Student
from src.messages import (
                          WHICH_PAIR_MESSAGE,
                          CHOOSE_PAIR_MESSAGE,
                          NO_LESSONS_TODAY)
from src.middlewares import CheckHeadmanMiddleware, CheckRegistrationMiddleware
from src.services import LessonService

__all__ = [
    "headman_router",
]


headman_router = Router()
headman_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=True))
headman_router.message.middleware(CheckHeadmanMiddleware(must_be_headman=True))
headman_router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях


@headman_router.message(Command("getstat"))
@logger.catch
async def getstat_command(message: Message, pool: Pool, student: Student) -> None:
    logger.trace("'/getstat' command started.")
    headman = student

    async with pool.acquire() as con:
        lesson_service = LessonService(con)
        lessons = await lesson_service.filter_by_student(headman)

        if not lessons:
            await message.answer(NO_LESSONS_TODAY)
            return

        await message.answer(CHOOSE_PAIR_MESSAGE, reply_markup=default_buttons(True))
        await message.answer(WHICH_PAIR_MESSAGE, reply_markup=choose_lesson_buttons(lessons))
