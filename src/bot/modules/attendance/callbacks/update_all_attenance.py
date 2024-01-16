from aiogram.types import CallbackQuery

from src.bot.common.router import RootRouter, Router
from src.modules.attendance.application.commands import UpdateAllAttendancesCommand
from src.modules.attendance.application.queries import GetStudentAttendanceQuery
from src.modules.student_management.domain import Student

from ..callback_data import UpdateAllAttendancesCallbackData
from ..resources.inline_buttons import attendance_buttons
from ..resources.templates import your_all_choice_is_template

__all__ = [
    "update_all_attendances_router",
]


update_all_attendances_router = Router(
    must_be_registered=True,
)
# update_attendance_router.callback_query.middleware(CheckInMiddleware())


def include_update_all_attendances_router(root_router: RootRouter) -> None:
    root_router.include_router(update_all_attendances_router)


@update_all_attendances_router.callback_query(UpdateAllAttendancesCallbackData.filter())
async def update_attendance(
    callback: CallbackQuery,
    callback_data: UpdateAllAttendancesCallbackData,
    student: Student,
    update_all_attendances_command: UpdateAllAttendancesCommand,
    get_student_attendance_query: GetStudentAttendanceQuery,
):
    if callback.message is None or callback.message.text is None:
        return

    await update_all_attendances_command.execute(student.id, student.is_checked_in_today, callback_data.new_status)

    new_attendances = await get_student_attendance_query.execute(student.id)
    new_text = your_all_choice_is_template(callback_data.new_status)

    if new_text == callback.message.html_text:
        await callback.answer(None)
    else:
        await callback.message.edit_text(
            text=new_text,
            reply_markup=attendance_buttons(True, new_attendances),
        )
