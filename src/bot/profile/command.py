from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.modules.student_management.application.queries import GetEduProfileInfoQuery
from src.modules.student_management.domain import Student

from .resources.templates import profile_info

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
        raise RuntimeError("Failed to fetch edu_info.")
    # await message.answer(text=profile_info(student.surname, student.name, student.role), reply_markup=profile_buttons())
    await message.answer(text=profile_info(student, edu_info))
