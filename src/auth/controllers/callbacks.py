from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from asyncpg.pool import PoolConnectionProxy
from loguru import logger

from src.auth.callback_data import (
    AccessCallbackData,
    RoleCallbackData,
    UniversityCallbackData,
)
from src.auth.controllers.registration_context import RegistrationContext
from src.auth.controllers.registration_states import RegistrationStates
from src.auth.resources.inline_buttons import university_list_buttons
from src.auth.resources.templates import (
    ASK_GROUP_TEMPLATE,
    ASK_UNIVERSITY_TEMPLATE,
    CHOOSE_STUDENT_ROLE_TEMPLATE,
    REGISTRATION_ACCEPTED_TEMPLATE,
    REGISTRATION_DENIED_TEMPLATE,
    YOU_WERE_ACCEPTED_TEMPLATE,
    YOU_WERE_DENIED_TEMPLATE,
    succesfull_role_choose_template,
    succesfull_university_choose_template,
)
from src.auth.services import CacheStudentService, RegistrationService
from src.bot import AuthContractService
from src.common.middlewares import (
    CheckRegistrationMiddleware,
    InjectDBConnectionMiddleware,
)
from src.common.resources.inline_buttons import inline_void_button

__all__ = [
    "registration_callbacks_router",
]


registration_callbacks_router = Router()
registration_callbacks_router.callback_query.outer_middleware(InjectDBConnectionMiddleware())
registration_callbacks_router.callback_query.middleware(CheckRegistrationMiddleware(must_be_registered=False))


@registration_callbacks_router.callback_query(AccessCallbackData.filter())
@logger.catch
async def accept_or_deny_callback(
    callback: CallbackQuery, callback_data: AccessCallbackData, bot: Bot, con: PoolConnectionProxy
) -> None:
    if callback.message is None:
        return

    async with CacheStudentService() as cache_student_service:
        student_data = await cache_student_service.pop_student_cache(callback_data.student_id)

    if not callback_data.accepted:
        await callback.message.edit_text(REGISTRATION_DENIED_TEMPLATE, reply_markup=inline_void_button())
        await bot.send_message(student_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    registration_service = RegistrationService(con)
    await registration_service.register_student(student_data)

    # await bot.send_message(
    #     user_data["telegram_id"], YOU_WERE_ACCEPTED_TEMPLATE, reply_markup=default_buttons(user_data["role"])
    # )
    await bot.send_message(callback_data.student_id, YOU_WERE_ACCEPTED_TEMPLATE)
    await callback.message.edit_text(REGISTRATION_ACCEPTED_TEMPLATE, reply_markup=inline_void_button())


@registration_callbacks_router.callback_query(RoleCallbackData.filter())
@logger.catch
async def get_role_from_user(
    callback: CallbackQuery, callback_data: RoleCallbackData, state: FSMContext, con: PoolConnectionProxy
) -> None:
    registration_ctx = RegistrationContext(state)

    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await registration_ctx.set_role(callback_data.role)

    await callback.message.edit_text(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=inline_void_button())
    await callback.message.answer(succesfull_role_choose_template(await registration_ctx.role))

    auth_contract_service = AuthContractService(con)
    universities = await auth_contract_service.get_all_universities()

    await callback.message.answer(text=ASK_UNIVERSITY_TEMPLATE, reply_markup=university_list_buttons(universities))
    await registration_ctx.set_state(RegistrationStates.waiting_university)


@registration_callbacks_router.callback_query(UniversityCallbackData.filter())
@logger.catch
async def get_university_from_user(
    callback: CallbackQuery, callback_data: UniversityCallbackData, state: FSMContext, con: PoolConnectionProxy
) -> None:
    registration_ctx = RegistrationContext(state)

    if callback.message is None:
        return

    auth_contract_service = AuthContractService(con)
    choosen_uni = await auth_contract_service.find_university_by_alias(callback_data.university_alias)

    await registration_ctx.set_university_alias(callback_data.university_alias)

    await callback.message.edit_text(ASK_UNIVERSITY_TEMPLATE, reply_markup=inline_void_button())
    await callback.message.answer(succesfull_university_choose_template(choosen_uni.name))
    await callback.message.answer(ASK_GROUP_TEMPLATE)

    await registration_ctx.set_state(RegistrationStates.waiting_group)
