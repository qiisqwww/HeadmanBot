from aiogram import Bot
from aiogram.types import CallbackQuery

from src.bot.common.resources import main_menu
from src.bot.common.router import RootRouter, Router
from src.bot.headman_panel.callback_data import ChooseStudentToEnhanceCallbackData
from src.bot.headman_panel.resources.templates import (
    FAILED_TO_GRANT_VICEHEADMAN_ROLE_TEMPLATE,
    STUDENT_WAS_NOT_FOUND_TEMPLATE,
    YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE,
)
from src.modules.student_management.application.commands.exceptions import (
    CannotGrantRoleToNonStudentError,
    StudentNotFoundError,
)
from src.modules.student_management.application.commands.make_student_viceheadman_command import (
    MakeStudentViceHeadmanCommand,
)
from src.modules.student_management.domain.enums.role import Role

set_vice_headman_router = Router(
    must_be_registered=True,
    minimum_role=Role.HEADMAN,
)


def include_set_vice_headman_router(root_router: RootRouter) -> None:
    root_router.include_router(set_vice_headman_router)


@set_vice_headman_router.callback_query(ChooseStudentToEnhanceCallbackData.filter())
async def set_vice_headman(
    callback: CallbackQuery,
    callback_data: ChooseStudentToEnhanceCallbackData,
    bot: Bot,
    make_student_vice_headman_command: MakeStudentViceHeadmanCommand,
) -> None:
    if callback.message is None:
        return

    try:
        await make_student_vice_headman_command.execute(
            callback_data.student_id,
        )

    except StudentNotFoundError:
        await callback.message.answer(STUDENT_WAS_NOT_FOUND_TEMPLATE)
        await callback.answer(None)
        return

    except CannotGrantRoleToNonStudentError:
        await callback.message.answer(FAILED_TO_GRANT_VICEHEADMAN_ROLE_TEMPLATE)
        await callback.answer(None)
        return

    await bot.send_message(
        callback_data.telegram_id,
        YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE,
        reply_markup=main_menu(Role.VICE_HEADMAN),
    )
    await callback.answer(None)
