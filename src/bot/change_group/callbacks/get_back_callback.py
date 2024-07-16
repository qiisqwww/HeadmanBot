from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupContext
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.change_group.callback_data import GetBackCallbackData
from src.bot.change_group.resources.templates import CHANGE_OR_QUIT_TEMPLATE
from src.bot.change_group.resources.inline_buttons import change_group_buttons

__all__ = [
    "include_get_back_callback_router",
]

get_back_callback_router = Router(
    must_be_registered=True
)


def include_get_back_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(get_back_callback_router)


@get_back_callback_router.callback_query(GetBackCallbackData.filter())
async def quit_group(callback: CallbackQuery, state: ChangeGroupContext) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(callback, CHANGE_OR_QUIT_TEMPLATE, reply_markup=change_group_buttons())
    await state.clear()
