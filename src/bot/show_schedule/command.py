from datetime import datetime

from aiogram.types import Message

from src.bot.common import CommandFilter, RootRouter, Router, TelegramCommand
from src.bot.show_schedule.resources.inline_buttons import show_schedule_buttons
from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.edu_info.application.queries.fetch_uni_alias_by_group_id_query import (
    FetchUniAliasByGroupIdQuery,
)
from src.modules.student_management.application.queries.get_edu_profile_info_query import (
    GetEduProfileInfoQuery,
)
from src.modules.student_management.domain import Student
from src.modules.utils.schedule_api.infrastructure.schedule_api import ScheduleApiImpl

from .resources import NO_LESSONS_TODAY_TEMPLATE, schedule_list_template

__all__ = [
    "include_get_schedule_command",
]


get_schedule_command_router = Router(
    must_be_registered=True,
)


def include_get_schedule_command(root_router: RootRouter) -> None:
    root_router.include_router(get_schedule_command_router)


@get_schedule_command_router.message(CommandFilter(TelegramCommand.SHOW_SCHEDULE))
async def get_attendance_command(
    message: Message,
    student: Student,
    timezone: str,
    fetch_uni_alias_query: FetchUniAliasByGroupIdQuery,
    fetch_group_name_query: GetEduProfileInfoQuery,
) -> None:
    uni_alias = await fetch_uni_alias_query.execute(student.group_id)
    group_name = await fetch_group_name_query.execute(student.group_id)
    schedule = await ScheduleApiImpl(uni_alias).fetch_schedule(group_name.group_name)

    if not schedule:
        await message.answer(
            NO_LESSONS_TODAY_TEMPLATE, reply_markup=show_schedule_buttons(),
        )
        return

    await message.answer(
        schedule_list_template(
            schedule,
            timezone,
            "сегодня",
            datetime.now().weekday(),
            uni_alias != UniversityAlias.BMSTU,
        ),
        reply_markup=show_schedule_buttons(),
    )
