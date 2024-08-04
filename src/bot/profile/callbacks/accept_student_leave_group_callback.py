from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import Bot
from aiogram.types import CallbackQuery, User

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import AcceptStudentLeaveGroupCallbackData
from src.bot.profile.resources.templates import (
    LEAVE_ACCEPTED_TEMPLATE,
    LEAVE_DENIED_TEMPLATE,
    SUCCESSFULLY_DID_NOT_LEFT_THE_GROUP_TEMPLATE,
    SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE,
    USER_WAS_NOT_FOUND_TO_EXPEL_TEMPLATE,
)
from src.modules.student_management.application.commands import ExpelUserFromGroupCommand
from src.modules.student_management.application.queries import FindStudentByTelegramIdQuery

__all__ = [
    "include_accept_student_leave_group_callback_router",
]


accept_student_leave_group_callback_router = Router(
    must_be_registered=True,
)


def include_accept_student_leave_group_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(accept_student_leave_group_callback_router)


@accept_student_leave_group_callback_router.callback_query(AcceptStudentLeaveGroupCallbackData.filter())
async def accept_or_deny_leave_group_callback(
    callback: CallbackQuery,
    callback_data: AcceptStudentLeaveGroupCallbackData,
    bot: Bot,
    expel_user_from_group_command: ExpelUserFromGroupCommand,
    find_student_by_telegram_id_query: FindStudentByTelegramIdQuery,
    inform_admins_about_exception: Callable[
        [Exception, User | None],
        Coroutine[Any, Any, None],
    ],
) -> None:
    if callback.message is None:
        return

    if not callback_data.accepted:
        await safe_message_edit(
            callback,
            LEAVE_DENIED_TEMPLATE,
        )
        await bot.send_message(callback_data.telegram_id, SUCCESSFULLY_DID_NOT_LEFT_THE_GROUP_TEMPLATE)
        return

    student = await find_student_by_telegram_id_query.execute(callback_data.telegram_id)
    if student is None:
        await safe_message_edit(
            callback,
            USER_WAS_NOT_FOUND_TO_EXPEL_TEMPLATE,
        )

    try:
        await expel_user_from_group_command.execute(student.id)
    except Exception as e:
        await inform_admins_about_exception(e, callback.from_user)
        return

    await bot.send_message(
        callback_data.telegram_id,
        SUCCESSFULLY_LEFT_THE_GROUP_TEMPLATE,
    )

    await safe_message_edit(callback, LEAVE_ACCEPTED_TEMPLATE)
