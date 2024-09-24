from aiogram.types import CallbackQuery

from src.bot.admin_panel.callback_data import CancelActionCallbackData
from src.bot.admin_panel.resources.templates import ACTION_WAS_CANCELLED_TEMPLATE
from src.bot.common import RootRouter, Router
from src.bot.common.contextes import DeleteStudentContext
from src.modules.common.infrastructure import DEBUG
from src.modules.student_management.domain.enums import Role

__all__ = [
    "include_cancel_action_router",
]

cancel_action_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT,
)


def include_cancel_action_router(root_router: RootRouter) -> None:
    root_router.include_router(cancel_action_router)


@cancel_action_router.callback_query(CancelActionCallbackData.filter())
async def cancel_action(callback: CallbackQuery, state: DeleteStudentContext) -> None:  # TODO INTERFACE FOR STATE
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.delete()
    await state.clear()

    await callback.message.answer(ACTION_WAS_CANCELLED_TEMPLATE)
    await callback.answer(None)
