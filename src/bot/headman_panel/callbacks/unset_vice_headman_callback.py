from aiogram import Bot
from aiogram.types import CallbackQuery
from src.modules.student_management.application.commands import (
    UnmakeStudentViceHeadmanCommand,
)
from src.modules.student_management.application.commands.exceptions import (
    CannotDowngradeNonViceHeadmanError,
    StudentNotFoundError,
)

from src.bot.common.resources import main_menu
from src.bot.common.router import RootRouter, Router
from src.bot.headman_panel.callback_data.choose_student_to_downgrade_callback_data import (
    ChooseStudentToDowngradeCallbackData,
)
from src.bot.headman_panel.resources.inline_buttons import select_student
from src.bot.headman_panel.resources.templates import (
    CHOOSE_USER_TO_DOWNGRADE_TEMPLATE,
    FAILED_TO_DOWNGRADE_VICEHEADMAN_ROLE_TEMPLATE,
    STUDENT_WAS_NOT_FOUND_TEMPLATE,
    USER_WAS_SUCCESSFULLY_DOWNGRADED,
    YOU_WAS_DOWNGRADED_TO_STUDENT_TEMPLATE,
)
from src.dto.entities.student import Student
from src.dto.enums.role import Role
from src.queries.get_students_from_group_query import (
    GetStudentsFromGroupQuery,
)

unset_vice_headman_router = Router(
    must_be_registered=True,
    minimum_role=Role.HEADMAN,
)


def include_unset_vice_headman_router(root_router: RootRouter) -> None:
    root_router.include_router(unset_vice_headman_router)


@unset_vice_headman_router.callback_query(ChooseStudentToDowngradeCallbackData.filter())
async def unset_vice_headman(
        callback: CallbackQuery,
        callback_data: ChooseStudentToDowngradeCallbackData,
        bot: Bot,
        student: Student,
        unmake_student_vice_headman_command: UnmakeStudentViceHeadmanCommand,
        get_students_by_group: GetStudentsFromGroupQuery,
) -> None:
    if callback.message is None:
        return

    try:
        await unmake_student_vice_headman_command.execute(
            callback_data.student_id,
        )

    except StudentNotFoundError:
        await callback.message.answer(STUDENT_WAS_NOT_FOUND_TEMPLATE)
        await callback.answer(None)
        return

    except CannotDowngradeNonViceHeadmanError:
        await callback.message.answer(FAILED_TO_DOWNGRADE_VICEHEADMAN_ROLE_TEMPLATE)
        await callback.answer(None)
        return

    students_list = await get_students_by_group.execute(student.group_id)
    students_list = list(
        filter(lambda s: s.id != callback_data.student_id, students_list),
    )
    await callback.message.edit_text(
        CHOOSE_USER_TO_DOWNGRADE_TEMPLATE,
        reply_markup=select_student(students_list, False),
    )
    await callback.message.answer(USER_WAS_SUCCESSFULLY_DOWNGRADED)

    await bot.send_message(
        callback_data.telegram_id,
        YOU_WAS_DOWNGRADED_TO_STUDENT_TEMPLATE,
        reply_markup=main_menu(Role.STUDENT),
    )
    await callback.answer(None)
