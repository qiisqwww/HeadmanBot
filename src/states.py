from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "RegStates",
    "SetHeadman",
]


class RegStates(StatesGroup):
    surname_input = State()
    name_input = State()
    group_input = State()


class SetHeadman(StatesGroup):
    get_password = State()
