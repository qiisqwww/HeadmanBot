from aiogram import Bot
from aiogram.types import CallbackQuery

from src.bot.common.resources import main_menu
from src.bot.common.router import RootRouter, Router
from src.bot.headman_panel.callback_data import ChooseStudentToEnhanceCallbackData
from src.bot.headman_panel.resources.inline_buttons import select_student
from src.bot.headman_panel.resources.templates import (
    CHOOSE_USER_TO_ENHANCE_TEMPLATE,
    FAILED_TO_GRANT_VICEHEADMAN_ROLE_TEMPLATE,
    STUDENT_WAS_NOT_FOUND_TEMPLATE,
    USER_WAS_SUCCESSFULLY_ENHANCED,
    YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE,
)
from src.modules.student_management.application.commands.exceptions import (
    CannotGrantRoleToNonStudentError,
    StudentNotFoundError,
)
from src.modules.student_management.application.commands.make_student_viceheadman_command import (
    MakeStudentViceHeadmanCommand,
)
from src.modules.student_management.application.queries import GetStudentsFromGroupQuery
from src.modules.student_management.domain import Role, Student

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
    student: Student,
    make_student_vice_headman_command: MakeStudentViceHeadmanCommand,
    get_students_by_group: GetStudentsFromGroupQuery,
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

    students_list = await get_students_by_group.execute(student.group_id)
    students_list = list(
        filter(lambda s: s.id != callback_data.student_id, students_list),
    )
    await callback.message.edit_text(
        CHOOSE_USER_TO_ENHANCE_TEMPLATE,
        reply_markup=select_student(students_list, True),
    )
    await callback.message.answer(USER_WAS_SUCCESSFULLY_ENHANCED)

    await bot.send_message(
        callback_data.telegram_id,
        YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE,
        reply_markup=main_menu(Role.VICE_HEADMAN),
    )
    await callback.answer(None)
