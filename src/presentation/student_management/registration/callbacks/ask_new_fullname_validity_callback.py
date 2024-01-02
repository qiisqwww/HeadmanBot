from aiogram import Bot
from aiogram.types import CallbackQuery

from src.application.student_management.commands.cache_create_student_data_command import (
    CacheCreateStudentDataCommand,
)
from src.application.student_management.queries import FindGroupHeadmanQuery
from src.application.student_management.repositories.create_student_dto import (
    CreateStudentDTO,
)
from src.domain.student_management import Role, StudentId
from src.infrastructure.common.config import ADMIN_IDS
from src.presentation.common.resources.void_inline_buttons import inline_void_button
from src.presentation.common.router import Router

from ..callback_data import AskNewFullnameValidityCallbackData
from ..registration_context import RegistrationContext
from ..registration_states import RegistrationStates
from ..resources.inline_buttons import accept_or_deny_buttons
from ..resources.templates import (
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
    headman_send_registration_request_template,
    student_send_registration_request_template,
)

__all__ = [
    "ask_new_fullname_validity_router",
]


ask_new_fullname_validity_router = Router(
    must_be_registered=False,
)


@ask_new_fullname_validity_router.callback_query(AskNewFullnameValidityCallbackData.filter())
async def ask_new_fullname_validity_callback(
    callback: CallbackQuery,
    callback_data: AskNewFullnameValidityCallbackData,
    state: RegistrationContext,
    bot: Bot,
    find_group_headman_query: FindGroupHeadmanQuery,
    cache_student_data_command: CacheCreateStudentDataCommand,
) -> None:
    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await callback.message.edit_text(
        f"Отлично, вы выбрали {'<b>да</b>' if callback_data.is_fullname_correct else '<b>нет</b>'}",
        reply_markup=inline_void_button(),
    )
    if not callback_data.is_fullname_correct:
        await callback.message.answer("Введите фамилию.", reply_markup=inline_void_button())
        await state.set_state(RegistrationStates.waiting_surname)
        return

    match await state.role:
        case Role.STUDENT:
            await callback.message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE, reply_markup=inline_void_button())
        case Role.HEADMAN:
            await callback.message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE, reply_markup=inline_void_button())

    student_data = await state.get_data()
    student_id = int(callback.from_user.id)
    await cache_student_data_command.execute(CreateStudentDTO(**student_data))

    surname = await state.surname
    name = await state.name
    if await state.role == Role.HEADMAN:
        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                headman_send_registration_request_template(name, surname),
                reply_markup=accept_or_deny_buttons(StudentId(student_id)),
            )
        return

    headman = await find_group_headman_query.execute(await state.group_name)

    if headman is None:
        raise RuntimeError("Group already must have a headman")

    await state.clear()

    await bot.send_message(
        headman.telegram_id,
        student_send_registration_request_template(surname, name),
        reply_markup=accept_or_deny_buttons(StudentId(student_id)),
    )
