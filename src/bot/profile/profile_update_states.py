from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "ProfileUpdateStates",
]


class ProfileUpdateStates(StatesGroup):
    waiting_new_surname = State()
    waiting_new_name = State()
    waiting_new_birthdate = State()
    on_validation = State()
