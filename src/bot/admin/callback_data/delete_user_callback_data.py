from aiogram.filters.callback_data import CallbackData

__all__ = [
    "DeleteStudentCallbackData",
]


class DeleteStudentCallbackData(CallbackData, prefix="delete_student_callback_data"):  # type: ignore
    ...
