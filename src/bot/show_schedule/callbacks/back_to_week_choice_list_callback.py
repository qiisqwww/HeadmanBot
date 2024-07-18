from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.show_schedule.resources.templates import CHOOSE_SCHEDULE_PERIOD_TEMPLATE
from src.bot.show_schedule.resources.inline_buttons import show_choose_period_buttons
from src.bot.show_schedule.callback_data import BackToWeekChoiceListCallbackData

__all__ = [
    "include_back_to_week_choice_list_callback_router",
]


back_to_week_choice_list_callback_router = Router(
    must_be_registered=True,
)


def include_back_to_week_choice_list_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(back_to_week_choice_list_callback_router)


@back_to_week_choice_list_callback_router.callback_query(BackToWeekChoiceListCallbackData.filter())
async def back_to_week_choice_list(callback: CallbackQuery) -> None:
    if callback.message is None:
        return

    await safe_message_edit(
        callback,
        CHOOSE_SCHEDULE_PERIOD_TEMPLATE,
        show_choose_period_buttons()
    )
