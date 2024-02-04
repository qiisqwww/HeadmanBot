from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "RegistrationStates",
]


class RegistrationStates(StatesGroup): # type: ignore [misc]
    waiting_role = State()
    waiting_university = State()
    waiting_group = State()
    waiting_birthdate = State()
    waiting_surname = State()
    waiting_name = State()
    ask_fullame_validity = State()
    on_verification = State()
