from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from asyncpg.pool import PoolConnectionProxy
from loguru import logger
from redis.asyncio import Redis

from src.modules.student.api.contracts import PermissionsServiceContract
from src.modules.student.internal.controllers.unregistred.registration_context import (
    RegistrationContext,
)
from src.modules.student.internal.controllers.unregistred.registration_states import (
    RegistrationStates,
)
from src.modules.student.internal.gateways import UniversityGatewate
from src.modules.student.internal.resources.inline_buttons import (
    university_list_buttons,
)
from src.modules.student.internal.resources.templates import (
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
from src.modules.student.internal.services import CacheStudentService, StudentService
from src.shared.middlewares import InjectStudentMiddleware
from src.shared.resources.inline_buttons import inline_void_button

from .callback_data import AccessCallbackData, RoleCallbackData, UniversityCallbackData

__all__ = [
    "registration_callbacks_router",
]


registration_callbacks_router = Router()
registration_callbacks_router.callback_query.middleware(
    InjectStudentMiddleware(must_be_registered=False, service=PermissionsServiceContract)
)


@registration_callbacks_router.callback_query(AccessCallbackData.filter())
@logger.catch
async def accept_or_deny_callback(
    callback: CallbackQuery, callback_data: AccessCallbackData, bot: Bot, con: PoolConnectionProxy, redis_con: Redis
) -> None:
    if callback.message is None:
        return

    cache_student_service = CacheStudentService(redis_con)
    student_data = await cache_student_service.pop_student_cache(callback_data.student_id)

    if not callback_data.accepted:
        await callback.message.edit_text(REGISTRATION_DENIED_TEMPLATE, reply_markup=inline_void_button())
        await bot.send_message(student_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    registration_service = StudentService(con)
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

    university_gateway = UniversityGatewate(con)
    universities = await university_gateway.get_all_universities()

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

    university_gateway = UniversityGatewate(con)
    choosen_uni = await university_gateway.find_university_by_alias(callback_data.university_alias)

    await registration_ctx.set_university_alias(callback_data.university_alias)

    await callback.message.edit_text(ASK_UNIVERSITY_TEMPLATE, reply_markup=inline_void_button())
    await callback.message.answer(succesfull_university_choose_template(choosen_uni.name))
    await callback.message.answer(ASK_GROUP_TEMPLATE)

    await registration_ctx.set_state(RegistrationStates.waiting_group)
