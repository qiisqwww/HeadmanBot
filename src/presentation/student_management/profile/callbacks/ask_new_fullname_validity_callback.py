from aiogram import Bot
from aiogram.types import CallbackQuery
from loguru import logger

from src.config.config import ADMIN_IDS
from src.dto.callback_data import AskNewFullnameValidityCallbackData
from src.dto.contexts import RegistrationContext
from src.dto.models import StudentId
from src.enums import Role
from src.handlers.states.registration_states import (
    RegistrationStates,
)
from src.kernel import Router
from src.resources.buttons.inline_buttons import accept_or_deny_buttons
from src.resources.buttons.void_inline_buttons import inline_void_button
from src.resources.templates.templates import (
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
    headman_send_registration_request_template,
    student_send_registration_request_template
)
from src.services import CacheStudentService, StudentService

__all__ = [
    "ask_new_fullname_validity_router",
]


ask_new_fullname_validity_router = Router(must_be_registered=False)


@ask_new_fullname_validity_router.callback_query(AskNewFullnameValidityCallbackData.filter())
@logger.catch
async def ask_new_fullname_validity_callback(
    callback: CallbackQuery,
    callback_data: AskNewFullnameValidityCallbackData,
    state: RegistrationContext,
    bot: Bot,
    cache_student_service: CacheStudentService,
    student_service: StudentService,
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
    await cache_student_service.cache_student(student_data)

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

    headman = await student_service.get_headman_by_group_name(await state.group_name)

    await state.clear()

    await bot.send_message(
        headman.telegram_id,
        student_send_registration_request_template(name, surname),
        reply_markup=accept_or_deny_buttons(StudentId(student_id)),
    )
