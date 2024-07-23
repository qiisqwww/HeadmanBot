from aiogram.types import Message

from src.bot.common import CommandFilter, RootRouter, Router, TelegramCommand
from src.bot.show_schedule.resources.templates import CHOOSE_SCHEDULE_PERIOD_TEMPLATE
from src.bot.show_schedule.resources.inline_buttons import show_choose_period_buttons
from src.modules.student_management.domain import Role, Student
from src.modules.edu_info.application.queries import FetchUniAliasByGroupIdQuery

__all__ = [
    "include_show_schedule_command_router",
]


show_schedule_command_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


def include_show_schedule_command_router(root_router: RootRouter) -> None:
    root_router.include_router(show_schedule_command_router)


@show_schedule_command_router.message(CommandFilter(TelegramCommand.SHOW_SCHEDULE))
async def get_attendance_command(
        message: Message,
        student: Student,
        fetch_uni_alias_by_group_id_query: FetchUniAliasByGroupIdQuery
) -> None:
    uni_alias = await fetch_uni_alias_by_group_id_query.execute(student.group_id)
    await message.answer(
        CHOOSE_SCHEDULE_PERIOD_TEMPLATE,
        reply_markup=show_choose_period_buttons(uni_alias)
    )
