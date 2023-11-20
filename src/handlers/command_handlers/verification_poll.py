from aiogram.fsm.context import FSMContext
from asyncpg.pool import Pool
from loguru import logger

from src.init_bot import bot
from src.config import ADMIN_ID_1, ADMIN_ID_2
from src.services import StudentService
from src.buttons import accept_or_deny_buttons
from src.services import GroupService, RedisService


@logger.catch
async def verify_registration(user_id: str, state: FSMContext, pool: Pool) -> None:
    user_data = await state.get_data()
    async with RedisService() as con:
        await con.insert_preregistration_user(user_data)

    if user_data["is_headman"] == "true":
        await bot.send_message(ADMIN_ID_1,
                               f"Староста {user_data['surname']} {user_data['name']} подал заявку на регистарцию в вашу группу",
                               reply_markup=accept_or_deny_buttons(user_id))
        await bot.send_message(ADMIN_ID_2,
                               f"Староста {user_data['surname']} {user_data['name']} подал заявку на регистарцию в вашу группу",
                               reply_markup=accept_or_deny_buttons(user_id))
        return

    async with pool.acquire() as con:
        group_service = GroupService(con)
        group = await group_service.get_by_name(user_data["group_name"])

        students_service = StudentService(con)
        students = await students_service.filter_by_group(group)

    headmans = [student for student in students if student.is_headman]

    for headman in headmans:
        await bot.send_message(headman.telegram_id,
                               f"Студент {user_data['surname']} {user_data['name']} подал заявку на регистарцию в вашу группу",
                               reply_markup=accept_or_deny_buttons(user_id))

    await state.clear()
