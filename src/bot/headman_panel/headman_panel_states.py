from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "HeadmanPanelStates",
]


class HeadmanPanelStates(StatesGroup):
    waiting_surname_and_name_for_set = State()
    waiting_surname_and_name_for_unset = State()
