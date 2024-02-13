from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup
from aiogram.types.callback_query import CallbackQuery

__all__ = [
    "safe_message_edit",
]


async def safe_message_edit(
    callback: CallbackQuery,
    new_text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    if callback.message is None:
        return

    try:
        await callback.message.edit_text(new_text, reply_markup=reply_markup)
    except TelegramBadRequest:
        await callback.answer(None)
