from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import SureToLeaveGroupCallbackData
from src.bot.profile.resources.templates import SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE, DID_NOT_LEFT_THE_GROUP_TEMPLATE
from src.modules.student_management.domain.models import Student
from src.modules.student_management.application.commands import ExpelUserFromGroupCommand


__all__ = [
    "include_ask_user_sure_to_leave_group_router",
]

ask_user_sure_to_leave_group_router = Router(
    must_be_registered=True
)


def include_ask_user_sure_to_leave_group_router(root_router: RootRouter) -> None:
    root_router.include_router(ask_user_sure_to_leave_group_router)


@ask_user_sure_to_leave_group_router.callback_query(SureToLeaveGroupCallbackData.filter())
async def ask_user_sure_to_leave_group(
        callback: CallbackQuery,
        callback_data: SureToLeaveGroupCallbackData,
        student: Student,
        expel_user_from_group_command: ExpelUserFromGroupCommand
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    if callback_data.is_user_sure:
        await expel_user_from_group_command.execute(student.id)
        await safe_message_edit(callback, SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE)
    else:
        await safe_message_edit(callback, DID_NOT_LEFT_THE_GROUP_TEMPLATE)
