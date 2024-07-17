from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "ChangeGroupStates",
]


class ChangeGroupStates(StatesGroup):
    waiting_new_group = State()
    waiting_new_role = State()
    on_verification = State()
