from aiogram import Bot
from aiogram.types import CallbackQuery

from src.bot.common.contextes import RegistrationContext
from src.bot.common.resources import void_inline_buttons
from src.bot.common.resources.templates import your_choice_is_template
from src.bot.common.router import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.registration.callback_data import AskNewFullnameValidityCallbackData
from src.bot.registration.finite_state.registration_states import RegistrationStates
from src.bot.registration.resources.inline_buttons import accept_or_deny_buttons
from src.bot.registration.resources.templates import (
    ASK_SURNAME_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
    student_send_registration_request_template,
)
from src.modules.common.infrastructure.config import ADMIN_IDS
from src.modules.student_management.application.commands import CacheCreateStudentDataCommand
from src.modules.student_management.application.queries import (
    FindGroupByNameAndAliasQuery,
    FindGroupHeadmanQuery,
)
from src.modules.student_management.application.repositories import CreateStudentDTO
from src.modules.student_management.domain import Role

__all__ = [
    "include_ask_new_fullname_validity_router",
]


ask_new_fullname_validity_router = Router()


def include_ask_new_fullname_validity_router(root_router: RootRouter) -> None:
    root_router.include_router(ask_new_fullname_validity_router)


@ask_new_fullname_validity_router.callback_query(
    AskNewFullnameValidityCallbackData.filter(),
)
async def ask_new_fullname_validity_callback(
    callback: CallbackQuery,
    callback_data: AskNewFullnameValidityCallbackData,
    state: RegistrationContext,
    bot: Bot,
    find_group_headman_query: FindGroupHeadmanQuery,
    find_group_by_name_and_alias_query: FindGroupByNameAndAliasQuery,
    cache_student_data_command: CacheCreateStudentDataCommand,
) -> None:
    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await safe_message_edit(
        callback,
        your_choice_is_template(callback_data.is_fullname_correct),
        reply_markup=void_inline_buttons(),
    )

    if not callback_data.is_fullname_correct:
        await callback.message.answer(
            ASK_SURNAME_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        await state.set_state(RegistrationStates.waiting_surname)
        return

    match await state.role:
        case Role.STUDENT:
            await callback.message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE)
        case Role.HEADMAN:
            await callback.message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE)

    student_data = await state.get_data()
    await cache_student_data_command.execute(CreateStudentDTO(**student_data))

    telegram_id = await state.telegram_id
    last_name = await state.last_name
    first_name = await state.first_name
    role = await state.role
    group_name = await state.group_name

    if role == Role.HEADMAN:
        await state.clear()
        await state.set_state(RegistrationStates.on_verification)
        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                student_send_registration_request_template(
                    last_name,
                    first_name,
                    role,
                    telegram_id,
                    group_name,
                    callback.from_user.username,
                ),
                reply_markup=accept_or_deny_buttons(telegram_id, callback.from_user.username),
            )
        return

    group = await find_group_by_name_and_alias_query.execute(
        await state.group_name,
        await state.university_alias,
    )

    if group is None:
        raise RuntimeError
    headman = await find_group_headman_query.execute(group.id)

    if headman is None:
        raise RuntimeError("Group already must have a headman")

    await state.clear()
    await state.set_state(RegistrationStates.on_verification)
    await bot.send_message(
        headman.telegram_id,
        student_send_registration_request_template(
            last_name,
            first_name,
            role,
            telegram_id,
            group_name,
            callback.from_user.username,
        ),
        reply_markup=accept_or_deny_buttons(telegram_id, callback.from_user.username),
    )
