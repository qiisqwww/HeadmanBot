from aiogram.types import ReplyKeyboardRemove

__all__ = [
    "remove_reply_buttons",
]


def remove_reply_buttons() -> ReplyKeyboardRemove:
    remove_markup = ReplyKeyboardRemove()

    return remove_markup
