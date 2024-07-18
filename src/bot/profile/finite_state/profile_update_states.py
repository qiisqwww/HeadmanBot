from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "ProfileUpdateStates",
]


class ProfileUpdateStates(StatesGroup):
    waiting_new_first_name = State()
    waiting_new_last_name = State()
    waiting_new_birthdate = State()
    waiting_new_uni = State()
    waiting_new_group = State()
    waiting_new_role = State()
    on_validation = State()
    on_verification = State()
