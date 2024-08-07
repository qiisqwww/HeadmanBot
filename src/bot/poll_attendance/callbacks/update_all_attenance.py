from aiogram.types import CallbackQuery

from src.bot.common.router import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.poll_attendance.callback_data import UpdateAllAttendancesCallbackData
from src.bot.poll_attendance.resources.inline_buttons import update_attendance_buttons
from src.bot.poll_attendance.resources.templates import your_all_choice_is_template
from src.modules.attendance.application.commands import UpdateAllAttendancesCommand
from src.modules.attendance.application.queries import GetStudentAttendanceQuery
from src.modules.student_management.domain import Role, Student

__all__ = [
    "include_update_all_attendances_router",
]


update_all_attendances_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT,
)


def include_update_all_attendances_router(root_router: RootRouter) -> None:
    root_router.include_router(update_all_attendances_router)


@update_all_attendances_router.callback_query(UpdateAllAttendancesCallbackData.filter())
async def update_attendance(
    callback: CallbackQuery,
    callback_data: UpdateAllAttendancesCallbackData,
    student: Student,
    update_all_attendances_command: UpdateAllAttendancesCommand,
    get_student_attendance_query: GetStudentAttendanceQuery,
    timezone: str,
) -> None:
    if callback.message is None or callback.message.text is None:
        return

    await update_all_attendances_command.execute(student.id, callback_data.new_status)

    new_attendances = await get_student_attendance_query.execute(student.id)
    new_text = your_all_choice_is_template(callback_data.new_status)

    await safe_message_edit(
        callback,
        new_text,
        update_attendance_buttons(True, new_attendances, timezone),
    )
