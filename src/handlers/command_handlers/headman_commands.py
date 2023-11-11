from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types.message import Message
from asyncpg import Pool
from loguru import logger

from src.buttons import load_choose_lesson_kb
from src.messages import (
    CHOOSE_GETSTAT_LESSON,
    FAQ_MESSAGE,
    HEADMAN_SEND_MSG_MISTAKE,
    NO_LESSONS_TODAY,
)
from src.middlewares import CheckHeadmanMiddleware, CheckRegistrationMiddleware
from src.mirea_api import MireaScheduleApi
from src.services.group_service import GroupService
from src.services.student_service import StudentService

__all__ = [
    "headman_router",
]


headman_router = Router()
headman_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=True))
headman_router.message.middleware(CheckHeadmanMiddleware(must_be_headman=True))
headman_router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях


@headman_router.message(Command("getstat"))
@logger.catch
async def getstat_command(message: Message, pool: Pool, api: MireaScheduleApi) -> None:
    logger.trace("'/getstat' command started.")
    if message.from_user is None:
        return

    user_id = message.from_user.id
    async with pool.acquire() as conn:
        student_service = StudentService(conn)
        group_service = GroupService(conn)

        headman = await student_service.get(user_id)
        group = await group_service.get(headman.group_id)

        if not await api.group_exists(group.name):
            await message.answer(HEADMAN_SEND_MSG_MISTAKE)
            return

        lessons = await student_service.get_schedule(user_id)

        if not lessons:
            await message.answer(NO_LESSONS_TODAY)
            return

        await message.answer(CHOOSE_GETSTAT_LESSON, reply_markup=load_choose_lesson_kb(lessons))


@headman_router.message(Command("faq"))
async def faq_command(message: types.Message) -> None:
    logger.trace("faq command")

    await message.answer(FAQ_MESSAGE, parse_mode=ParseMode.MARKDOWN)
