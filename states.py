from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

__all__ = ["RegStates"]

class RegStates(StatesGroup):
    name_input = State()
    surname_input = State()
    group_input = State()
    registered = State()
