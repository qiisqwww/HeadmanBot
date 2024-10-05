from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "ChangeGroupAdminStates",
]


class ChangeGroupAdminStates(StatesGroup):
    waiting_university = State()
    waiting_group = State()
