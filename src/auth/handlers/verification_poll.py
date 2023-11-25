from aiogram import Bot
from aiogram.fsm.context import FSMContext
from asyncpg.pool import Pool
from loguru import logger

from src.buttons import accept_or_deny_buttons
from src.config import ADMIN_IDS
from src.enums.role import Role
from src.services import RedisService

__all__ = [
    "verify_registration",
]


@logger.catch
async def verify_registration(state: FSMContext, pool: Pool, bot: Bot) -> None:
    user_data = await state.get_data()
    async with RedisService() as con:
        await con.insert_preregistration_user(user_data)

    if user_data["role"] is Role.HEADMAN:
        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                f"Староста {user_data['surname']} {user_data['name']} подал заявку на регистарцию в боте.",
                reply_markup=accept_or_deny_buttons(user_data["telegram_id"]),
            )
        return

    # async with pool.acquire() as con:
    #     group_service = GroupService(con)
    #     group = await group_service.get_by_name(user_data["group_name"])
    #
    #     students_service = StudentService(con)
    #     students = await students_service.filter_by_group(group)
    #
    # headmans = [student for student in students if student.is_headman]
    #
    # for headman in headmans:
    #     await bot.send_message(
    #         headman.telegram_id,
    #         f"Студент {user_data['surname']} {user_data['name']} подал заявку на регистарцию в вашу группу",
    #         reply_markup=accept_or_deny_buttons(user_id),
    #     )

    await state.clear()
