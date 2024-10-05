from aiogram.filters.callback_data import CallbackData

from src.modules.common.domain import UniversityAlias

__all__ = [
    "ChooseUniCallbackData",
]


class ChooseUniCallbackData(CallbackData, prefix="choose new uni (only for admins)"):  # type: ignore
    university_alias: UniversityAlias
