from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.headman_panel.callback_data import SetViceHeadmanCallbackData
from src.bot.headman_panel.resources.inline_buttons import select_student
from src.bot.headman_panel.resources.templates import CHOOSE_USER_TO_ENHANCE_TEMPLATE
from src.modules.student_management.application.queries import GetStudentsFromGroupQuery
from src.modules.student_management.domain import Role, Student

__all__ = [
    "include_choose_student_to_enhance_router",
]


choose_student_to_enhance_router = Router(
    must_be_registered=True,
    minimum_role=Role.HEADMAN,
)


def include_choose_student_to_enhance_router(root_router: RootRouter) -> None:
    root_router.include_router(choose_student_to_enhance_router)


@choose_student_to_enhance_router.callback_query(SetViceHeadmanCallbackData.filter())
async def choose_student_to_enhance_callback(
    callback: CallbackQuery,
    student: Student,
    get_student_by_group: GetStudentsFromGroupQuery,
) -> None:
    if callback.message is None:
        return

    students_list = await get_student_by_group.execute(student.group_id)
    await callback.message.answer(
        CHOOSE_USER_TO_ENHANCE_TEMPLATE,
        reply_markup=select_student(students_list, enhance_to_vice_headman=True),
    )

    await callback.answer(None)
