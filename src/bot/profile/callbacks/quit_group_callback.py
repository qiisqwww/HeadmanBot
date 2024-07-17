from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.profile.callback_data import QuitGroupCallbackData
from src.bot.profile.resources.templates import SURE_TO_LEAVE_GROUP_TEMPLATE
from src.bot.profile.resources.inline_buttons import sure_to_leave_group_buttons
from src.modules.student_management.domain.models import Student


__all__ = [
    "include_quit_group_callback_router",
]

quit_group_callback_router = Router(
    must_be_registered=True
)


def include_quit_group_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(quit_group_callback_router)


@quit_group_callback_router.callback_query(QuitGroupCallbackData.filter())
async def quit_group(callback: CallbackQuery) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.answer(
        SURE_TO_LEAVE_GROUP_TEMPLATE,
        reply_markup=sure_to_leave_group_buttons()
    )
