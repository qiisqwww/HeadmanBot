from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AskEditedFullnameValidityCallbackData",
]


class AskEditedFullnameValidityCallbackData(CallbackData, prefix="ask_fullname_while_editing"):  # type: ignore
    is_fullname_correct: bool
