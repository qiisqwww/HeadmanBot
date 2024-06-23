from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "ScheduleDateStates",
]


class ScheduleDateStates(StatesGroup):
    waiting_date = State()
