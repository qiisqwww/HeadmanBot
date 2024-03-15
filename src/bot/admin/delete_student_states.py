from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "DeleteStudentStates",
]


class DeleteStudentStates(StatesGroup):
    waiting_telegram_id = State()
    waiting_fullname_group = State()
