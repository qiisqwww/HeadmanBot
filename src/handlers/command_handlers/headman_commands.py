from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from loguru import logger

from src.buttons import load_choose_lesson_kb
from src.messages import (
    CHOOSE_GETSTAT_LESSON,
    FAQ_MESSAGE,
    HEADMAN_SEND_MSG_MISTAKE,
    NO_LESSONS_TODAY,
    LOOK_WHAT_I_FOUND_MESSAGE
)
from src.middlewares import CheckHeadmanMiddleware, CheckRegistrationMiddleware
from src.mirea_api import MireaScheduleApi
from src.services.group_service import GroupService
from src.services.student_service import StudentService
from src.buttons import load_headman_kb

__all__ = [
    "headman_router",
]


headman_router = Router()

headman_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=True))
headman_router.message.middleware.register(CheckHeadmanMiddleware(must_be_headman=True))

headman_router.message.filter(F.chat.type.in_({"private"}))  # Бот будет отвечать только в личных сообщениях


@headman_router.message(Command("getstat"))
@logger.catch
async def getstat_command(message: types.Message) -> None:
    logger.trace("getstat command")
    api = MireaScheduleApi()

    user_id = message.from_user.id

    async with StudentService() as student_service:
        headman = await student_service.get(user_id)

        async with GroupService() as group_service:
            group = await group_service.get(headman.group_id)

        if not await api.group_exists(group.name):
            await message.answer(HEADMAN_SEND_MSG_MISTAKE)
            return

        lessons = await student_service.get_schedule(user_id)

        if not lessons:
            await message.answer(NO_LESSONS_TODAY)
            return

        await message.answer(LOOK_WHAT_I_FOUND_MESSAGE, reply_markup = load_headman_kb())
        await message.answer(CHOOSE_GETSTAT_LESSON, reply_markup=load_choose_lesson_kb(lessons))


@headman_router.message(Command("faq"))
async def faq_command(message: types.Message) -> None:
    logger.trace("faq command")

    await message.answer(FAQ_MESSAGE, parse_mode=ParseMode.MARKDOWN)
