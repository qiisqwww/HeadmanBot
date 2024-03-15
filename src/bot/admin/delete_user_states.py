from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "DeleteUserStates",
]


class DeleteUserStates(StatesGroup):
    waiting_telegram_id = State()
    waiting_fullname_group = State()
