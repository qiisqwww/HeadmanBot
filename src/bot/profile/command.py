from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.modules.student_management.application.queries import GetEduProfileInfoQuery
from src.modules.student_management.domain import Student

from .resources.inline_buttons import profile_buttons
from .resources.templates import FAILED_TO_LOAD_EDU_INFO_TEMPLATE, profile_info

__all__ = [
    "include_profile_command_router",
]


profile_router = Router(
    must_be_registered=True,
)


def include_profile_command_router(root_router: RootRouter) -> None:
    root_router.include_router(profile_router)


@profile_router.message(CommandFilter(TelegramCommand.PROFILE))
async def profile_command(
    message: Message,
    student: Student,
    get_edu_profile_info_query: GetEduProfileInfoQuery,
) -> None:
    edu_info = await get_edu_profile_info_query.execute(student.group_id)

    if edu_info is None:
        await message.answer(FAILED_TO_LOAD_EDU_INFO_TEMPLATE)
        return

    await message.answer(text=profile_info(student, edu_info), reply_markup=profile_buttons())
