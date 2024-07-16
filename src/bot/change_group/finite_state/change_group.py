from datetime import date

from aiogram import F
from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupContext
from src.bot.change_group.finite_state.change_group_states import ChangeGroupStates


__all__ = [
    "include_change_group_fsm_router"
]


change_group_fsm_router = Router(
    must_be_registered=True,
)


def include_change_group_fsm_router(root_router: RootRouter) -> None:
    root_router.include_router(change_group_fsm_router)


@change_group_fsm_router.message(F.text, ChangeGroupStates.waiting_new_group)
async def new_group_handler(message: Message, state: ChangeGroupContext) -> None:
    if message.text is None:
        return

    await state.set_state(ChangeGroupStates.waiting_new_role)


@change_group_fsm_router.message(F.text, ChangeGroupStates.waiting_new_role)
async def new_role_handler(message: Message, state: ChangeGroupContext) -> None:
    if message.text is None:
        return

    await state.clear()
