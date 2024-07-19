from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.poll_attendance.callback_data import UpdateAttendanceCallbackData
from src.bot.poll_attendance.resources.templates import your_all_choice_is_template, your_choice_is_template
from src.bot.poll_attendance.resources.inline_buttons import  update_attendance_buttons
from src.modules.attendance.application.commands import UpdateAttendanceCommand
from src.modules.attendance.application.queries import GetStudentAttendanceQuery
from src.modules.student_management.domain import Student, Role

__all__ = [
    "include_update_attendance_router",
]


update_attendance_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


def include_update_attendance_router(root_router: RootRouter) -> None:
    root_router.include_router(update_attendance_router)


@update_attendance_router.callback_query(UpdateAttendanceCallbackData.filter())
async def update_attendance(
    callback: CallbackQuery,
    callback_data: UpdateAttendanceCallbackData,
    student: Student,
    update_attendance_command: UpdateAttendanceCommand,
    get_student_attendance_query: GetStudentAttendanceQuery,
    timezone: str,
) -> None:
    if callback.message is None or callback.message.text is None:
        return

    await update_attendance_command.execute(
        student.id,
        callback_data.attendance_id,
        callback_data.new_status,
    )

    new_attendances = await get_student_attendance_query.execute(student.id)
    choosen_attendance = next(
        filter(
            lambda attendance: attendance.id == callback_data.attendance_id,
            new_attendances,
        ),
    )

    if all(
        choosen_attendance.status == attendance.status for attendance in new_attendances
    ):
        new_text = your_all_choice_is_template(choosen_attendance.status)
    else:
        new_text = your_choice_is_template(choosen_attendance, timezone)

    await safe_message_edit(
        callback,
        new_text,
        reply_markup=update_attendance_buttons(True, new_attendances, timezone),
    )
