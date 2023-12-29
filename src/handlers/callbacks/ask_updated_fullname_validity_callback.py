from aiogram.types import CallbackQuery
from loguru import logger

from src.dto.callback_data import AskEditedFullnameValidityCallbackData
from src.dto.contexts import EditingContext
from src.dto.models import StudentId
from src.enums import Role
from src.handlers.finite_state.profile_updater.updater_states import UpdaterStates
from src.kernel import Router
from src.resources import inline_void_button, ASK_SURNAME_TEMPLATE
from src.services import StudentService

__all__ = [
    "ask_updated_fullname_validity_router",
]


ask_updated_fullname_validity_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


@ask_updated_fullname_validity_router.callback_query(AskEditedFullnameValidityCallbackData.filter())
@logger.catch
async def ask_new_fullname_validity_callback(
    callback: CallbackQuery,
    callback_data: AskEditedFullnameValidityCallbackData,
    state: EditingContext,
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
        await callback.message.answer(
            ASK_SURNAME_TEMPLATE,
            reply_markup=inline_void_button()
        )
        await state.set_state(UpdaterStates.waiting_surname)
        return

    student_id = callback.from_user.id
    surname = await state.surname
    name = await state.name

    await student_service.update_fullname_by_id(surname, name, StudentId(student_id))

    await state.clear()
