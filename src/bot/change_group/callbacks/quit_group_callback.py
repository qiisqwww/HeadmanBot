from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupContext
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.change_group.callback_data import QuitGroupCallbackData
from src.bot.change_group.resources.templates import YOU_LEFT_GROUP_TEMPLATE
from src.bot.change_group.finite_state.change_group_states import ChangeGroupStates

__all__ = [
    "include_quit_group_callback_router",
]

quit_group_callback_router = Router()


def include_quit_group_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(quit_group_callback_router)


@quit_group_callback_router.callback_query(QuitGroupCallbackData.filter())
async def quit_group(callback: CallbackQuery, state: ChangeGroupContext) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await safe_message_edit(callback, YOU_LEFT_GROUP_TEMPLATE)
    await state.set_state(ChangeGroupStates.waiting_new_group)
