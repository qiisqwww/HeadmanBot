from aiogram import F, Router
from aiogram.types.callback_query import CallbackQuery
from asyncpg import Pool
from loguru import logger

from src.init_bot import bot
from src.services import RedisService, StudentService
from src.buttons import (
    inline_void_button,
    default_buttons,
    remove_reply_buttons
)
from src.messages import (
    REGISTRATION_DENIED_MESSAGE,
    REGISTRATION_ACCEPTED_MESSAGE,
    YOU_WERE_DENIED_MESSAGE,
    YOU_WERE_ACCEPTED_MESSAGE
)

__all__ = ["verification_callback_router"]


verification_callback_router = Router()


@verification_callback_router.callback_query(F.data.startswith("reg_"))
async def accept_or_deny_callback(callback: CallbackQuery, pool: Pool) -> None:
    if callback.data is None:
        logger.error("No callback data for accept or deny.")
        return

    prefix, status, user_id = callback.data.split('_')

    async with RedisService() as con:
        user_data = await con.get_and_remove_user(user_id)

    if status == "denied":
        await callback.message.edit_text(REGISTRATION_DENIED_MESSAGE,
                                         reply_markup=inline_void_button())
        await bot.send_message(int(user_data["telegram_id"]), YOU_WERE_DENIED_MESSAGE)
        return

    if user_data["is_headman"] == 'true':
        is_headman = True
    else:
        is_headman = False

    logger.info(user_data)

    async with pool.acquire() as con:
        student_service = StudentService(con)
        await student_service.register(telegram_id=int(user_data["telegram_id"]),
                                       name=user_data["name"],
                                       surname=user_data["surname"],
                                       university_id=int(user_data["university_id"]),
                                       group_name=user_data["group_name"],
                                       is_headman=is_headman)
        await bot.send_message(int(user_data["telegram_id"]),
                                YOU_WERE_ACCEPTED_MESSAGE,
                                reply_markup=default_buttons(is_headman))

    await callback.message.edit_text(REGISTRATION_ACCEPTED_MESSAGE,
                                     reply_markup=inline_void_button())
