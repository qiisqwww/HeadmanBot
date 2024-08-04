from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import Bot
from aiogram.types import CallbackQuery, User

from src.bot.common import RootRouter, Router
from src.bot.common.resources import main_menu, void_inline_buttons
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import AcceptStudentEnterGroupCallbackData
from src.bot.profile.resources.templates import (
    ENTER_ACCEPTED_TEMPLATE,
    ENTER_DENIED_TEMPLATE,
    FAILED_TO_FETCH_SCHEDULE_TEMPLATE,
    HELP_FOR_HEADMAN,
    USER_GROUP_ENTER_TIME_OUT_TEMPLATE,
    USER_HAS_ALREADY_ENTERED_GROUP_TEMPLATE,
    YOU_WERE_ACCEPTED_TEMPLATE,
    YOU_WERE_DENIED_TEMPLATE,
)
from src.modules.student_management.application.commands import (
    ClearStudentEnterGroupDataCommand,
    NotFoundStudentEnterGroupCachedDataError,
    StudentAlreadyEnteredGroupError,
    StudentEnterGroupCommand,
)
from src.modules.student_management.domain.enums.role import Role
from src.modules.utils.schedule_api.infrastructure.exceptions import ScheduleApiError

__all__ = [
    "include_accept_student_enter_group_callback_router",
]


accept_student_enter_group_callback_router = Router(
    must_be_registered=True,
)


def include_accept_student_enter_group_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(accept_student_enter_group_callback_router)


@accept_student_enter_group_callback_router.callback_query(AcceptStudentEnterGroupCallbackData.filter())
async def accept_or_deny_enter_group_callback(
    callback: CallbackQuery,
    callback_data: AcceptStudentEnterGroupCallbackData,
    bot: Bot,
    clear_student_enter_group_data_command: ClearStudentEnterGroupDataCommand,
    student_enter_group_command: StudentEnterGroupCommand,
    inform_admins_about_exception: Callable[
        [Exception, User | None],
        Coroutine[Any, Any, None],
    ],
) -> None:
    if callback.message is None:
        return

    if not callback_data.accepted:
        await clear_student_enter_group_data_command.execute(callback_data.telegram_id)
        await safe_message_edit(
            callback,
            ENTER_DENIED_TEMPLATE,
        )
        await bot.send_message(callback_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    try:
        student = await student_enter_group_command.execute(callback_data.telegram_id)
    except ScheduleApiError as e:
        await safe_message_edit(
            callback,
            FAILED_TO_FETCH_SCHEDULE_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        await bot.send_message(
            callback_data.telegram_id,
            FAILED_TO_FETCH_SCHEDULE_TEMPLATE,
        )
        await inform_admins_about_exception(e, callback.from_user)
        return
    except StudentAlreadyEnteredGroupError:
        await safe_message_edit(
            callback,
            USER_HAS_ALREADY_ENTERED_GROUP_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        return
    except NotFoundStudentEnterGroupCachedDataError:
        await safe_message_edit(
            callback,
            USER_GROUP_ENTER_TIME_OUT_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        return

    await bot.send_message(
        callback_data.telegram_id,
        YOU_WERE_ACCEPTED_TEMPLATE,
        reply_markup=main_menu(student.role),
    )

    if student.role == Role.HEADMAN:
        await bot.send_message(
            callback_data.telegram_id,
            HELP_FOR_HEADMAN,
            reply_markup=main_menu(student.role),
        )
    await safe_message_edit(
        callback,
        ENTER_ACCEPTED_TEMPLATE,
        void_inline_buttons(),
    )
