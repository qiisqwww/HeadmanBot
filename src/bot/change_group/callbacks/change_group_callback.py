from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupContext
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.change_group.callback_data import ChangeGroupCallbackData
from src.bot.change_group.resources.templates import INPUT_NEW_GROUP_TEMPLATE
from src.bot.change_group.resources.inline_buttons import get_back_button
from src.bot.change_group.finite_state.change_group_states import ChangeGroupStates

__all__ = [
    "include_change_group_callback_router",
]

change_group_callback_router = Router()


def include_change_group_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(change_group_callback_router)


@change_group_callback_router.callback_query(ChangeGroupCallbackData.filter())
async def change_group(callback: CallbackQuery, state: ChangeGroupContext) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(callback, INPUT_NEW_GROUP_TEMPLATE, reply_markup=get_back_button())
    await state.set_state(ChangeGroupStates.waiting_new_group)
