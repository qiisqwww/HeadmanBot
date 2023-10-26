from aiogram.fsm.state import StatesGroup, State

__all__ = ["RegStates", "SetHeadMen"]


class RegStates(StatesGroup):
    surname_input = State()
    group_input = State()


class SetHeadMen(StatesGroup):
    get_password = State()