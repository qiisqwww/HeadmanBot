from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "UpdaterStates",
]


class UpdaterStates(StatesGroup):
    waiting_surname = State()
    waiting_name = State()
