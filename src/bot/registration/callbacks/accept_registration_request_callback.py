from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import Bot
from aiogram.types import CallbackQuery, User

from src.bot.common import RootRouter, Router
from src.bot.common.resources import main_menu, void_inline_buttons
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.registration.callback_data import AcceptRegistrationCallbackData
from src.bot.registration.resources.templates import (
    FAILED_TO_FETCH_SCHEDULE_TEMPLATE,
    HELP_FOR_HEADMAN,
    REGISTRATION_ACCEPTED_TEMPLATE,
    REGISTRATION_DENIED_TEMPLATE,
    YOU_WERE_ACCEPTED_TEMPLATE,
    YOU_WERE_DENIED_TEMPLATE,
    USER_HAS_ALREADY_BEEN_REGISTERED_TEMPLATE,
    USER_REGISTRATION_TIME_OUT_TEMPLATE
)
from src.modules.student_management.application.commands import (
    ClearCreateStudentDataCacheCommand,
    NotFoundStudentRegistrationCachedDataError,
    RegisterStudentCommand,
    StudentAlreadyRegisteredError,
)
from src.modules.student_management.domain.enums.role import Role
from src.modules.utils.schedule_api.infrastructure.exceptions import ScheduleApiError

__all__ = [
    "include_accept_registration_callback_router",
]


accept_registration_callback_router = Router(
    must_be_registered=None,
)


def include_accept_registration_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(accept_registration_callback_router)


@accept_registration_callback_router.callback_query(AcceptRegistrationCallbackData.filter())
async def accept_or_deny_callback(
    callback: CallbackQuery,
    callback_data: AcceptRegistrationCallbackData,
    bot: Bot,
    clear_create_student_data_command: ClearCreateStudentDataCacheCommand,
    register_student_command: RegisterStudentCommand,
    inform_admins_about_exception: Callable[
        [Exception, User | None],
        Coroutine[Any, Any, None],
    ],
) -> None:
    if callback.message is None:
        return

    if not callback_data.accepted:
        await clear_create_student_data_command.execute(callback_data.telegram_id)
        await safe_message_edit(
            callback,
            REGISTRATION_DENIED_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        await bot.send_message(callback_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    try:
        student = await register_student_command.execute(callback_data.telegram_id)
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
    except StudentAlreadyRegisteredError:
        await safe_message_edit(
            callback,
            USER_HAS_ALREADY_BEEN_REGISTERED_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        return
    except NotFoundStudentRegistrationCachedDataError:
        await safe_message_edit(
            callback,
            USER_REGISTRATION_TIME_OUT_TEMPLATE,
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
        REGISTRATION_ACCEPTED_TEMPLATE,
        void_inline_buttons(),
    )
