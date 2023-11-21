from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "RegistrationStates",
]


class RegistrationStates(StatesGroup):
    waiting_university = State()
    waiting_group = State()
    waiting_role = State()
    waiting_surname = State()
    waiting_name = State()
    on_verification = State()
