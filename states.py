from aiogram.fsm.state import StatesGroup, State

__all__ = ["RegStates", "SetHeadMen", "ReqPars"]


class RegStates(StatesGroup):
    surname_input = State()
    group_input = State()


class SetHeadMen(StatesGroup):
    get_password = State()


class ReqPars(StatesGroup):
    group_input_req = State()
    another_group_input = State()
