from datetime import datetime, timedelta

from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.show_schedule.resources import (
    CHOOSE_DATE_TEMPLATE,
    show_choose_day_buttons
)
from src.bot.show_schedule.callback_data import ScheduleWeekCallbackData
from src.modules.edu_info.application.queries.fetch_uni_alias_by_group_id_query import FetchUniAliasByGroupIdQuery
from src.modules.student_management.application.queries.get_edu_profile_info_query import GetEduProfileInfoQuery
from src.modules.student_management.domain import Student

__all__ = [
    "include_show_schedule_week_callback_router",
]


show_schedule_week_callback_router = Router(
    must_be_registered=True,
)


def include_show_schedule_week_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(show_schedule_week_callback_router)


@show_schedule_week_callback_router.callback_query(ScheduleWeekCallbackData.filter())
async def show_chosen_week_schedule_callback(
    callback: CallbackQuery,
    callback_data: ScheduleWeekCallbackData,
) -> None:
    if callback.message is None:
        return

    await safe_message_edit(
        callback,
        CHOOSE_DATE_TEMPLATE,
        show_choose_day_buttons(callback_data.weeks_to_add)
    )
