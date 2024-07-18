from datetime import date

from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.show_schedule.resources.templates import (
    NO_LESSONS_TODAY_TEMPLATE,
    schedule_list_template
)
from src.bot.show_schedule.resources.inline_buttons import show_choose_day_buttons
from src.bot.show_schedule.callback_data import ScheduleDateCallbackData
from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.edu_info.application.queries.fetch_uni_alias_by_group_id_query import FetchUniAliasByGroupIdQuery
from src.modules.student_management.application.queries.get_edu_profile_info_query import GetEduProfileInfoQuery
from src.modules.student_management.domain import Student
from src.modules.utils.schedule_api.infrastructure.schedule_api import ScheduleApiImpl

__all__ = [
    "include_show_schedule_date_callback_router",
]


show_schedule_date_callback_router = Router(
    must_be_registered=True,
)


def include_show_schedule_date_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(show_schedule_date_callback_router)


@show_schedule_date_callback_router.callback_query(ScheduleDateCallbackData.filter())
async def show_chosen_date_schedule_callback(
    callback: CallbackQuery,
    callback_data: ScheduleDateCallbackData,
    student: Student,
    timezone: str,
    fetch_uni_alias_query: FetchUniAliasByGroupIdQuery,
    fetch_group_name_query: GetEduProfileInfoQuery,
) -> None:
    if callback.message is None:
        return

    uni_alias = await fetch_uni_alias_query.execute(student.group_id)
    group_name = await fetch_group_name_query.execute(student.group_id)
    chosen_day = callback_data.chosen_day
    schedule = await ScheduleApiImpl(uni_alias).fetch_schedule(
        group_name.group_name,
        day=chosen_day,
    )

    if not schedule:
        await safe_message_edit(
            callback,
            NO_LESSONS_TODAY_TEMPLATE,
            show_choose_day_buttons(callback_data.weeks_to_add)
        )
        return

    await safe_message_edit(
        callback,
        schedule_list_template(
            schedule,
            timezone,
            "сегодня" if chosen_day == date.today() else str(chosen_day),
            chosen_day.weekday(),
            uni_alias != UniversityAlias.BMSTU,
        ),
        show_choose_day_buttons(callback_data.weeks_to_add)
    )
