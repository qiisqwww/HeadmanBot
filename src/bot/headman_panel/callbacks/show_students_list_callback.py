from aiogram.types import CallbackQuery
from loguru import logger

from src.bot.common.router import RootRouter, Router
from src.bot.headman_panel.callback_data import ShowStudentListCallbackData
from src.bot.headman_panel.resources.templates import students_list
from src.modules.student_management.application.queries import (
    GetStudentsFromGroupQuery,
)
from src.modules.student_management.domain import Role, Student

show_students_list_router = Router(
    must_be_registered=True,
    minimum_role=Role.VICE_HEADMAN,
)


def include_show_students_list_router(root_router: RootRouter) -> None:
    root_router.include_router(show_students_list_router)


@show_students_list_router.callback_query(ShowStudentListCallbackData.filter())
async def show_students_list(
    callback: CallbackQuery,
    student: Student,
    get_students_query: GetStudentsFromGroupQuery,
) -> None:
    students = await get_students_query.execute(student.group_id)
    await callback.message.answer(students_list(students))
    await callback.answer(None)