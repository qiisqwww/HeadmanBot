from datetime import date

from aiogram import Bot, Router
from aiogram.types.callback_query import CallbackQuery
from asyncpg import Pool
from loguru import logger

from src.buttons import default_buttons, inline_void_button
from src.enums.role import Role
from src.handlers.callback_data import AccessCallbackFactory
from src.messages import (
    REGISTRATION_ACCEPTED_MESSAGE,
    REGISTRATION_DENIED_MESSAGE,
    YOU_WERE_ACCEPTED_MESSAGE,
    YOU_WERE_DENIED_MESSAGE,
)
from src.middlewares import CheckRegistrationMiddleware
from src.services import GroupService, RedisService, StudentService, UniversityService

__all__ = [
    "verification_callback_router",
]


verification_callback_router = Router()
verification_callback_router.callback_query.middleware(CheckRegistrationMiddleware(must_be_registered=False))


@verification_callback_router.callback_query(AccessCallbackFactory.filter())
@logger.catch
async def accept_or_deny_callback(
    callback: CallbackQuery, callback_data: AccessCallbackFactory, pool: Pool, bot: Bot
) -> None:
    if callback.message is None:
        return

    async with RedisService() as con:
        user_data = await con.get_and_remove_user(str(callback_data.student_id))

    if not callback_data.accepted:
        await callback.message.edit_text(REGISTRATION_DENIED_MESSAGE, reply_markup=inline_void_button())
        await bot.send_message(int(user_data["telegram_id"]), YOU_WERE_DENIED_MESSAGE)
        return

    async with pool.acquire() as con:
        student_service = StudentService(con)
        group_service = GroupService(con)
        university_service = UniversityService(con)

        new_student = await student_service.register(
            telegram_id=int(user_data["telegram_id"]),
            name=user_data["name"],
            surname=user_data["surname"],
            birthday=0,
            birthmonth=0,
        )

        if user_data["role"] == Role.HEADMAN:
            university = await university_service.find_by_alias(user_data["university_alias"])
            new_group = await group_service.create(
                user_data["group_name"],
                int(user_data["telegram_id"]),
                university.id,
                date(day=1, month=1, year=3000),  # FIXME: Set correct payment data. It is neccecary for payment work.
            )
        else:
            new_group = await group_service.get_by_name(user_data["group_name"])

        await group_service.append_student_to_group(new_group, new_student)

    await bot.send_message(
        user_data["telegram_id"], YOU_WERE_ACCEPTED_MESSAGE, reply_markup=default_buttons(user_data["role"])
    )
    await callback.message.edit_text(REGISTRATION_ACCEPTED_MESSAGE, reply_markup=inline_void_button())


from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from asyncpg import Pool
from loguru import logger

from src.buttons import inline_void_button, university_list_buttons
from src.handlers.callback_data import RolesCallbackFactory, UniversitiesCallbackFactory
from src.messages import (
    ASK_GROUP_MESSAGE,
    ASK_UNIVERSITY,
    CHOOSE_STUDENT_ROLE,
    SUCCESFULL_ROLE_CHOOSE,
    SUCCESFULL_UNIVERSITY_CHOOSE,
)
from src.middlewares import CheckRegistrationMiddleware
from src.reg_states import RegistrationStates
from src.registration_context import RegistrationContext
from src.services import UniversityService

registration_callbacks_router = Router()
registration_callbacks_router.callback_query.middleware(CheckRegistrationMiddleware(must_be_registered=False))


@registration_callbacks_router.callback_query(RolesCallbackFactory.filter())
@logger.catch
async def get_role_from_user(
    callback: CallbackQuery, callback_data: RolesCallbackFactory, state: FSMContext, pool: Pool
) -> None:
    registration_ctx = RegistrationContext(state)

    if callback.message is None:
        return

    await registration_ctx.set_role(callback_data.role)
    await callback.message.edit_text(CHOOSE_STUDENT_ROLE, reply_markup=inline_void_button())
    await callback.message.answer(SUCCESFULL_ROLE_CHOOSE.format(role=callback_data.role))

    async with pool.acquire() as con:
        university_service = UniversityService(con)
        universities = await university_service.all()

    await callback.message.answer(text=ASK_UNIVERSITY, reply_markup=university_list_buttons(universities))

    await registration_ctx.set_state(RegistrationStates.waiting_university)


@registration_callbacks_router.callback_query(UniversitiesCallbackFactory.filter())
@logger.catch
async def get_university_from_user(
    callback: CallbackQuery, callback_data: UniversitiesCallbackFactory, state: FSMContext, pool: Pool
) -> None:
    registration_ctx = RegistrationContext(state)

    if callback.message is None:
        return

    async with pool.acquire() as con:
        university_service = UniversityService(con)
        choosen_uni = await university_service.find_by_alias(callback_data.university_alias)

    await registration_ctx.set_university_alias(callback_data.university_alias)

    await callback.message.edit_text(ASK_UNIVERSITY, reply_markup=inline_void_button())
    await callback.message.answer(SUCCESFULL_UNIVERSITY_CHOOSE.format(uni=choosen_uni.name))

    await callback.message.answer(ASK_GROUP_MESSAGE)

    await registration_ctx.set_state(RegistrationStates.waiting_group)
