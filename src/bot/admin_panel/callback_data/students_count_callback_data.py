from aiogram.filters.callback_data import CallbackData

__all__ = [
    "StudentsCountCallbackData",
]


class StudentsCountCallbackData(CallbackData, prefix="get_students_count"):  # type: ignore
    ...
