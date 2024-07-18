from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import LeaveGroupCallbackData
from src.bot.profile.resources.templates import SURE_TO_LEAVE_GROUP_TEMPLATE
from src.bot.profile.resources.inline_buttons import sure_to_leave_group_buttons


__all__ = [
    "include_leave_group_callback_router",
]

leave_group_callback_router = Router(
    must_be_registered=True
)


def include_leave_group_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(leave_group_callback_router)


@leave_group_callback_router.callback_query(LeaveGroupCallbackData.filter())
async def leave_group(callback: CallbackQuery) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(
        callback,
        SURE_TO_LEAVE_GROUP_TEMPLATE,
        reply_markup=sure_to_leave_group_buttons()
    )
