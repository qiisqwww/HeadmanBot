from datetime import date

from aiogram import F
from aiogram.types import Message
from src.modules.student_management.domain import Role, Student

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ScheduleCertainDateContext
from src.bot.show_schedule.finite_state.schedule_date_states import ScheduleDateStates
from src.bot.show_schedule.resources.inline_buttons import show_get_back_button
from src.bot.show_schedule.resources.templates import (
    INCORRECT_DATE_FORMAT_TEMPLATE,
    NO_LESSONS_TODAY_TEMPLATE,
    schedule_list_template,
)
from src.queries.fetch_uni_alias_by_group_id_query import FetchUniAliasByGroupIdQuery
from src.queries.get_edu_profile_info_query import GetEduProfileInfoQuery
from src.utils.schedule_api.infrastructure import ScheduleApiImpl

__all__ = [
    "include_show_schedule_certain_date_router",
]

show_schedule_certain_date_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT,
)


def include_show_schedule_certain_date_router(root_router: RootRouter) -> None:
    root_router.include_router(show_schedule_certain_date_router)


@show_schedule_certain_date_router.message(F.text, ScheduleDateStates.waiting_date)
async def handling_certain_date(
        message: Message,
        state: ScheduleCertainDateContext,
        student: Student,
        timezone: str,
        fetch_uni_alias_query: FetchUniAliasByGroupIdQuery,
        fetch_group_name_query: GetEduProfileInfoQuery,
) -> None:
    if message.text is None:
        return

    try:
        day, month, year = map(int, message.text.split("."))
        certain_date = date(year=year, month=month, day=day)

        uni_alias = await fetch_uni_alias_query.execute(student.group_id)
        group_name = await fetch_group_name_query.execute(student.group_id)
        schedule = await ScheduleApiImpl(uni_alias).fetch_schedule(
            group_name.group_name,
            day=certain_date,
        )

        if not schedule:
            await message.answer(NO_LESSONS_TODAY_TEMPLATE, reply_markup=show_get_back_button())
            return

        await message.answer(
            schedule_list_template(
                schedule,
                timezone,
                "сегодня" if certain_date == date.today() else str(certain_date),
                certain_date.weekday()
            ),
            reply_markup=show_get_back_button(),
        )
    except Exception:
        await message.answer(INCORRECT_DATE_FORMAT_TEMPLATE)
        await state.set_state(ScheduleDateStates.waiting_date)
        return

    await state.clear()
