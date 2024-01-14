from aiogram.filters.callback_data import CallbackData

__all__ = [
    "UpdateAttendanceCallbackData",
]


class UpdateAttendanceCallbackData(CallbackData, prefix="update_attendace_prefix"):  # type: ignore
    all: bool | None = None
    lesson_id: int | None = None
    # day_of_poll: date
