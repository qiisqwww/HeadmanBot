from aiogram.filters.callback_data import CallbackData

from src.common import UniversityAlias

__all__ = [
    "ChooseUniCallbackData",
]


class ChooseUniCallbackData(CallbackData, prefix="choose_new_university"):  # type: ignore
    university_alias: UniversityAlias
