from aiogram.types import CallbackQuery
from loguru import logger

from src.dto.callback_data import AskUpdatedFieldValidityCallbackData
from src.dto.contexts import ProfileUpdateContext
from src.dto.models import Student
from src.enums import Role, ProfileField
from src.handlers.states import ProfileUpdateStates
from src.kernel import Router
from src.resources import (
    inline_void_button,
    ASK_NEW_SURNAME_TEMPLATE,
    ASK_NEW_NAME_TEMPLATE,
    your_choice_is_template,
    main_menu
)
from src.services import StudentService

__all__ = [
    "ask_updated_fullname_validity_router",
]


ask_updated_fullname_validity_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


@ask_updated_fullname_validity_router.callback_query(AskUpdatedFieldValidityCallbackData.filter())
@logger.catch
async def ask_new_fullname_validity_callback(
    callback: CallbackQuery,
    callback_data: AskUpdatedFieldValidityCallbackData,
    state: ProfileUpdateContext,
    student_service: StudentService,
    student: Student
) -> None:
    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await callback.message.edit_text(
        your_choice_is_template(callback_data.is_field_correct),
        reply_markup=inline_void_button(),
    )

    if not callback_data.is_field_correct:
        if callback_data.field_type == ProfileField.name:
            await callback.message.answer(
                text=ASK_NEW_NAME_TEMPLATE,
                reply_markup=main_menu(student.role)
            )
            await state.set_state(ProfileUpdateStates.waiting_new_name)
            return
        else:
            await callback.message.answer(
                text=ASK_NEW_SURNAME_TEMPLATE,
                reply_markup=main_menu(student.role)
            )
            await state.set_state(ProfileUpdateStates.waiting_new_surname)
            return

    if callback_data.field_type == ProfileField.name:
        new_name = await state.name
        await student_service.update_name_by_id(new_name, student.telegram_id)
    else:
        new_surname = await state.surname
        await student_service.update_surname_by_id(new_surname, student.telegram_id)

    await state.clear()
