from aiogram import Bot
from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import SureToLeaveGroupCallbackData
from src.bot.profile.resources.templates import (
    YOUR_APPLY_TO_LEAVE_WAS_SENT_TO_HEADMAN_TEMPLATE,
    DID_NOT_LEFT_THE_GROUP_TEMPLATE,
    student_send_leave_group_request_template
)
from src.bot.profile.resources.inline_buttons import accept_or_deny_leave_group_buttons
from src.modules.student_management.domain.models import Student
from src.modules.student_management.application.queries import FindGroupHeadmanQuery


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
        bot: Bot,
        find_group_headman_query: FindGroupHeadmanQuery,

) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    if not callback_data.is_user_sure:
        await safe_message_edit(callback, DID_NOT_LEFT_THE_GROUP_TEMPLATE)
        return

    await safe_message_edit(callback, YOUR_APPLY_TO_LEAVE_WAS_SENT_TO_HEADMAN_TEMPLATE)

    group_headman = await find_group_headman_query.execute(student.group_id)
    await bot.send_message(
        group_headman.telegram_id,
        student_send_leave_group_request_template(
            student.last_name,
            student.first_name,
            student.role,
            student.telegram_id,
            callback.from_user.username
        ),
        reply_markup=accept_or_deny_leave_group_buttons(student.telegram_id)
    )


