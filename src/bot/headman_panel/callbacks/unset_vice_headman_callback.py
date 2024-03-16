from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.headman_panel.callback_data import UnsetViceHeadmanCallbackData
from src.bot.headman_panel.headman_panel_states import HeadmanPanelStates
from src.modules.student_management.domain import Role

__all__ = [
    "include_unset_vice_headman_router",
]


unset_vice_headman_router = Router(
    must_be_registered=True,
    minimum_role=Role.HEADMAN,
)


def include_unset_vice_headman_router(root_router: RootRouter) -> None:
    root_router.include_router(unset_vice_headman_router)


@unset_vice_headman_router.callback_query(UnsetViceHeadmanCallbackData.filter())
async def unset_vice_headman_callback(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if callback.message is None:
        return

    await callback.message.answer(
        "Введите фамилию имя пользователя, которого хотите сделать замом, через пробел.",
    )

    await state.set_state(HeadmanPanelStates.waiting_surname_and_name_for_unset)
    await callback.answer(None)
