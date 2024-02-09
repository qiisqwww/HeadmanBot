from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "ProfileUpdateStates",
]


class ProfileUpdateStates(StatesGroup):
    waiting_new_first_name = State()
    waiting_new_last_name = State()
    waiting_new_birthdate = State()
    on_validation = State()
