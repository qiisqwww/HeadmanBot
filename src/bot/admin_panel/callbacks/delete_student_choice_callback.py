from aiogram.types import CallbackQuery

from src.bot.admin_panel.callback_data import (
    DeleteByNameAndGroupCallbackData,
    DeleteByTGIDCallbackData,
)
from src.bot.admin_panel.finite_state.delete_student_states import DeleteStudentStates
from src.bot.admin_panel.resources.inline_buttons import cancel_button
from src.bot.admin_panel.resources.templates import (
    INPUT_FULLNAME_GROUP_TEMPLATE,
    INPUT_STUDENT_TG_ID_TEMPLATE,
)
from src.bot.common import RootRouter, Router
from src.bot.common.contextes import DeleteStudentContext
from src.common.infrastructure import DEBUG
from src.modules.student_management.domain.enums import Role

__all__ = [
    "include_delete_student_choice_router",
]

delete_student_choice_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT,
)


def include_delete_student_choice_router(root_router: RootRouter) -> None:
    root_router.include_router(delete_student_choice_router)


@delete_student_choice_router.callback_query(DeleteByTGIDCallbackData.filter())
async def ask_user_telegram_id(
        callback: CallbackQuery,
        state: DeleteStudentContext,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.answer(
        text=INPUT_STUDENT_TG_ID_TEMPLATE,
        reply_markup=cancel_button(),
    )
    await state.set_state(DeleteStudentStates.waiting_telegram_id)

    await callback.answer(None)


@delete_student_choice_router.callback_query(DeleteByNameAndGroupCallbackData.filter())
async def ask_user_fullname_group_name(
        callback: CallbackQuery,
        state: DeleteStudentContext,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.answer(
        text=INPUT_FULLNAME_GROUP_TEMPLATE,
        reply_markup=cancel_button(),
    )
    await state.set_state(DeleteStudentStates.waiting_fullname_group)

    await callback.answer(None)
