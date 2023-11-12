from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types.message import Message
from asyncpg import Pool
from loguru import logger

from src.buttons import load_choose_lesson_kb
from src.dto import Student
from src.messages import CHOOSE_GETSTAT_LESSON, FAQ_MESSAGE, NO_LESSONS_TODAY
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

        await message.answer(CHOOSE_GETSTAT_LESSON, reply_markup=load_choose_lesson_kb(lessons))


@headman_router.message(Command("faq"))
async def faq_command(message: types.Message) -> None:
    logger.trace("faq command")

    await message.answer(FAQ_MESSAGE, parse_mode=ParseMode.MARKDOWN)
