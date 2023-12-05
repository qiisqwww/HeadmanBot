@callbacks_router.callback_query(UpdateAttendanceCallbackData.filter())
@logger.catch
async def update_attendance(
    callback: CallbackQuery,
    callback_data: UpdateAttendanceCallbackData,
    student: StudentDTO,
    attendance_service: AttendanceService,
):
    if callback.message is None:
        return

    if callback_data.all is not None and callback_data.all:
        await attendance_service.update_visit_status_by_student_id(student.telegram_id, VisitStatus.VISIT)
        await callback.message.edit_text(ALL_MESSAGE, reply_markup=inline_void_button())
        return

    if callback_data.all is not None and not callback_data.all:
        await attendance_service.update_visit_status_by_student_id(student.telegram_id, VisitStatus.NOT_VISIT)
        await callback.message.edit_text(NONE_MESSAGE, reply_markup=inline_void_button())
        return

    if callback_data.all is None or callback_data.lesson_id is None:
        raise TypeError("Incorrect buttons usage")

    await attendance_service.update_visit_status(student.telegram_id, callback_data.lesson_id, VisitStatus.VISIT)
    attendances = await attendance_service.filter_by_student_id(student.telegram_id)

    choosen_lesson = next(
        filter(lambda attendance: attendance.lesson.id == callback_data.lesson_id, attendances)
    ).lesson
    non_visit_lessons = [attendance.lesson for attendance in attendances if attendance.status != VisitStatus.VISIT]

    if non_visit_lessons:
        keyboard = attendance_buttons(non_visit_lessons)
        text = f"Вы посетите пару {choosen_lesson.name}, которая начнётся в {choosen_lesson.str_start_time}"
    else:
        keyboard = inline_void_button()
        text = ALL_MESSAGE

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
    )
