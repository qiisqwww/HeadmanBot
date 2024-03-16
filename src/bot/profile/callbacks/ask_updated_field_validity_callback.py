from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ProfileUpdateContext
from src.bot.common.resources import main_menu, void_inline_buttons
from src.bot.common.resources.templates import your_choice_is_template
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import (
    AskUpdatedBirthdateValidityCallbackData,
    AskUpdatedNameValidityCallbackData,
    AskUpdatedSurnameValidityCallbackData,
)
from src.bot.profile.profile_update_states import ProfileUpdateStates
from src.bot.profile.resources.inline_buttons import profile_buttons
from src.bot.profile.resources.templates import (
    ASK_NEW_BIRTHDATE_TEMPLATE,
    ASK_NEW_NAME_TEMPLATE,
    ASK_NEW_SURNAME_TEMPLATE,
    profile_info,
)
from src.modules.student_management.application.commands import (
    UpdateStudentFirstNameCommand,
    UpdateStudentLastNameCommand,
)
from src.modules.student_management.application.commands.update_student_birthdate_command import (
    UpdateStudentBirthdateCommand,
)
from src.modules.student_management.application.queries import GetEduProfileInfoQuery
from src.modules.student_management.domain import Student

__all__ = [
    "include_ask_updated_field_validity_router",
]


ask_updated_field_validity_router = Router(
    must_be_registered=True,
)


def include_ask_updated_field_validity_router(root_router: RootRouter) -> None:
    root_router.include_router(ask_updated_field_validity_router)


@ask_updated_field_validity_router.callback_query(
    AskUpdatedNameValidityCallbackData.filter(),
)
async def ask_new_first_name_validity_callback(
    callback: CallbackQuery,
    callback_data: AskUpdatedNameValidityCallbackData,
    state: ProfileUpdateContext,
    student: Student,
    get_edu_profile_info_query: GetEduProfileInfoQuery,
    update_student_first_name_command: UpdateStudentFirstNameCommand,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(
        callback,
        your_choice_is_template(callback_data.is_field_correct),
        reply_markup=void_inline_buttons(),
    )

    if not callback_data.is_field_correct:
        await callback.message.answer(
            text=ASK_NEW_NAME_TEMPLATE,
            reply_markup=main_menu(student.role),
        )
        await state.set_state(ProfileUpdateStates.waiting_new_first_name)
        return

    await update_student_first_name_command.execute(
        student.id,
        await state.new_first_name,
    )

    edu_info = await get_edu_profile_info_query.execute(student.group_id)
    new_student = Student(
        id=student.id,
        telegram_id=student.telegram_id,
        first_name=await state.new_first_name,
        last_name=student.last_name,
        role=student.role,
        group_id=student.group_id,
        birthdate=student.birthdate,
        attendance_noted=student.attendance_noted,
    )
    await callback.message.answer(
        text=profile_info(new_student, edu_info),
        reply_markup=profile_buttons(),
    )

    await state.clear()


@ask_updated_field_validity_router.callback_query(
    AskUpdatedSurnameValidityCallbackData.filter(),
)
async def ask_new_last_name_validity_callback(
    callback: CallbackQuery,
    callback_data: AskUpdatedSurnameValidityCallbackData,
    state: ProfileUpdateContext,
    student: Student,
    get_edu_profile_info_query: GetEduProfileInfoQuery,
    update_student_last_name_command: UpdateStudentLastNameCommand,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(
        callback,
        your_choice_is_template(callback_data.is_field_correct),
        reply_markup=void_inline_buttons(),
    )

    if not callback_data.is_field_correct:
        await callback.message.answer(
            text=ASK_NEW_SURNAME_TEMPLATE,
            reply_markup=main_menu(student.role),
        )
        await state.set_state(ProfileUpdateStates.waiting_new_last_name)
        return

    await update_student_last_name_command.execute(
        student.id,
        await state.new_last_name,
    )

    new_student = Student(
        id=student.id,
        telegram_id=student.telegram_id,
        first_name=student.first_name,
        last_name=await state.new_last_name,
        role=student.role,
        group_id=student.group_id,
        birthdate=student.birthdate,
        attendance_noted=student.attendance_noted,
    )
    edu_info = await get_edu_profile_info_query.execute(student.group_id)
    await callback.message.answer(
        text=profile_info(new_student, edu_info),
        reply_markup=profile_buttons(),
    )

    await state.clear()


@ask_updated_field_validity_router.callback_query(
    AskUpdatedBirthdateValidityCallbackData.filter(),
)
async def ask_new_birthdate_validity_callback(
    callback: CallbackQuery,
    callback_data: AskUpdatedBirthdateValidityCallbackData,
    state: ProfileUpdateContext,
    student: Student,
    get_edu_profile_info_query: GetEduProfileInfoQuery,
    update_student_birthdate_command: UpdateStudentBirthdateCommand,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(
        callback,
        your_choice_is_template(callback_data.is_field_correct),
        reply_markup=void_inline_buttons(),
    )

    if not callback_data.is_field_correct:
        await callback.message.answer(
            text=ASK_NEW_BIRTHDATE_TEMPLATE,
            reply_markup=main_menu(student.role),
        )
        await state.set_state(ProfileUpdateStates.waiting_new_birthdate)
        return

    await update_student_birthdate_command.execute(
        student.id,
        await state.new_birthdate,
    )

    new_student = Student(
        id=student.id,
        telegram_id=student.telegram_id,
        first_name=student.first_name,
        last_name=student.last_name,
        role=student.role,
        group_id=student.group_id,
        birthdate=await state.new_birthdate,
        attendance_noted=student.attendance_noted,
    )
    edu_info = await get_edu_profile_info_query.execute(student.group_id)
    await callback.message.answer(
        text=profile_info(new_student, edu_info),
        reply_markup=profile_buttons(),
    )

    await state.clear()
