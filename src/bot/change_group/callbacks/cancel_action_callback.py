from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.change_group.callback_data import CancelActionCallbackData
from src.bot.change_group.resources.templates import ACTION_CANCELLED_TEMPLATE

__all__ = [
    "include_cancel_action_router",
]

cancel_action_router = Router(
    must_be_registered=True
)


def include_cancel_action_router(root_router: RootRouter) -> None:
    root_router.include_router(cancel_action_router)


@cancel_action_router.callback_query(CancelActionCallbackData.filter())
async def cancel_action(callback: CallbackQuery) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(callback, ACTION_CANCELLED_TEMPLATE)