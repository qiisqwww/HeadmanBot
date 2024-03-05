from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.show_schedule.resources.inline_buttons import show_schedule_buttons
from src.bot.show_schedule.resources.templates import (
    NO_LESSONS_TODAY_TEMPLATE,
    schedule_list_template,
)
from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.edu_info.application.queries.fetch_uni_alias_by_group_id_query import (
    FetchUniAliasByGroupIdQuery,
)
from src.modules.student_management.application.queries.get_edu_profile_info_query import (
    GetEduProfileInfoQuery,
)
from src.modules.student_management.domain import Student
from src.modules.utils.schedule_api.infrastructure.schedule_api import ScheduleApiImpl

__all__ = [
    "include_show_today_schedule_callback",
]


choose_lesson_callback_router = Router(
    must_be_registered=True,
)


def include_show_today_schedule_callback(root_router: RootRouter) -> None:
    root_router.include_router(choose_lesson_callback_router)


@choose_lesson_callback_router.callback_query(F.data == "show_schedule_today")
async def show_today_schedule_callback(
    callback: CallbackQuery,
    student: Student,
    timezone: str,
    fetch_uni_alias_query: FetchUniAliasByGroupIdQuery,
    fetch_group_name_query: GetEduProfileInfoQuery,
) -> None:
    if callback.message is None:
        return

    uni_alias = await fetch_uni_alias_query.execute(student.group_id)
    group_name = await fetch_group_name_query.execute(student.group_id)
    schedule = await ScheduleApiImpl(uni_alias).fetch_schedule(
        group_name.group_name,
    )

    if not schedule:
        await callback.message.edit_text(NO_LESSONS_TODAY_TEMPLATE)
        return

    await safe_message_edit(
        callback,
        schedule_list_template(
            schedule,
            timezone,
            "сегодня",
            datetime.now().weekday(),
            uni_alias != UniversityAlias.BMSTU,
        ),
        reply_markup=show_schedule_buttons(),
    )
