from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

__all__ = ["RegStates"]

class RegStates(StatesGroup):
    surname_input = State()
    group_input = State()


class SetHeadMen(StatesGroup):
    get_password = State()
