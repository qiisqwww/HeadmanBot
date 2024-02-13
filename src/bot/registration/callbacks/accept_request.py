from aiogram import Bot
from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.resources import main_menu, void_inline_buttons
from src.bot.registration.callback_data import AccessCallbackData
from src.bot.registration.resources.templates import (
    FAILED_TO_FETCH_SCHEDULE_TEMPLATE,
    REGISTRATION_ACCEPTED_TEMPLATE,
    REGISTRATION_DENIED_TEMPLATE,
    YOU_WERE_ACCEPTED_TEMPLATE,
    YOU_WERE_DENIED_TEMPLATE,
)
from src.modules.student_management.application.commands import (
    ClearCreateStudentDataCacheCommand,
    NotFoundStudentCachedDataError,
    RegisterStudentCommand,
    StudentAlreadyRegisteredError,
)
from src.modules.utils.schedule_api.infrastructure.exceptions import ScheduleApiError

__all__ = [
    "include_access_callback_router",
]


access_callback_router = Router(
    must_be_registered=None,
)


def include_access_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(access_callback_router)


@access_callback_router.callback_query(AccessCallbackData.filter())
async def accept_or_deny_callback(
    callback: CallbackQuery,
    callback_data: AccessCallbackData,
    bot: Bot,
    clear_create_student_data_command: ClearCreateStudentDataCacheCommand,
    register_student_command: RegisterStudentCommand,
) -> None:
    if callback.message is None:
        return

    if not callback_data.accepted:
        await clear_create_student_data_command.execute(callback_data.telegram_id)
        await callback.message.edit_text(
            REGISTRATION_DENIED_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        await bot.send_message(callback_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    try:
        student = await register_student_command.execute(callback_data.telegram_id)
    except ScheduleApiError:
        await callback.message.edit_text(
            FAILED_TO_FETCH_SCHEDULE_TEMPLATE,
            reply_markup=void_inline_buttons(),
        )
        await bot.send_message(
            callback_data.telegram_id,
            FAILED_TO_FETCH_SCHEDULE_TEMPLATE,
        )
        return
    except StudentAlreadyRegisteredError:
        await callback.message.edit_text(
            "Пользователь уже был зарегистрирован.",
            reply_markup=void_inline_buttons(),
        )
        return
    except NotFoundStudentCachedDataError:
        await callback.message.edit_text(
            "Данные пользователя не были найдены в кеше. Они хранятся только 1 неделю",
            reply_markup=void_inline_buttons(),
        )
        return

    await bot.send_message(
        callback_data.telegram_id,
        YOU_WERE_ACCEPTED_TEMPLATE,
        reply_markup=main_menu(student.role),
    )
    await callback.message.edit_text(
        REGISTRATION_ACCEPTED_TEMPLATE,
        reply_markup=void_inline_buttons(),
    )
