from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.show_schedule.resources import INPUT_CERTAIN_DATE_TEMPLATE, show_get_back_button
from src.bot.show_schedule.finite_state import ScheduleDateStates
from src.bot.common.contextes import ScheduleCertainDateContext
from src.bot.show_schedule.callback_data import ScheduleCertainDayCallbackData

__all__ = [
    "include_ask_certain_date_schedule_router",
]

ask_certain_date_schedule_router = Router(
    must_be_registered=True,
)


def include_ask_certain_date_schedule_router(root_router: RootRouter) -> None:
    root_router.include_router(ask_certain_date_schedule_router)


@ask_certain_date_schedule_router.callback_query(ScheduleCertainDayCallbackData.filter())
async def show_chosen_date_schedule_callback(
        callback: CallbackQuery,
        state: ScheduleCertainDateContext
) -> None:
    if callback.message is None:
        return

    await safe_message_edit(callback, INPUT_CERTAIN_DATE_TEMPLATE, show_get_back_button())
    await state.set_state(ScheduleDateStates.waiting_date)
