from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.bot.common.command_filter import TelegramCommand
from src.modules.student_management.domain import Role

__all__ = [
    "main_menu",
]


def admin_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text=TelegramCommand.ADMIN))
    builder.row(KeyboardButton(text=TelegramCommand.SHOW_ATTENDANCE))

    builder.row(
        KeyboardButton(text=TelegramCommand.SHOW_SCHEDULE),
        KeyboardButton(text=TelegramCommand.PROFILE),
    )

    builder.row(
        KeyboardButton(text=TelegramCommand.GROUP_PANEL),
        KeyboardButton(text=TelegramCommand.HELP),
    )

    return builder.as_markup(resize_keyboard=True)


def headman_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text=TelegramCommand.SHOW_ATTENDANCE))

    builder.row(
        KeyboardButton(text=TelegramCommand.SHOW_SCHEDULE),
        KeyboardButton(text=TelegramCommand.PROFILE),
    )

    builder.row(
        KeyboardButton(text=TelegramCommand.GROUP_PANEL),
        KeyboardButton(text=TelegramCommand.HELP),
    )

    return builder.as_markup(resize_keyboard=True)


def vice_headman_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text=TelegramCommand.SHOW_ATTENDANCE))

    builder.row(
        KeyboardButton(text=TelegramCommand.SHOW_SCHEDULE),
        KeyboardButton(text=TelegramCommand.PROFILE),
    )

    builder.row(
        KeyboardButton(text=TelegramCommand.HELP),
    )

    return builder.as_markup(resize_keyboard=True)


def student_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=TelegramCommand.SHOW_SCHEDULE),
        KeyboardButton(text=TelegramCommand.PROFILE),
    )

    builder.row(
        KeyboardButton(text=TelegramCommand.HELP),
    )

    return builder.as_markup(resize_keyboard=True)


def main_menu(role: Role) -> ReplyKeyboardMarkup:
    match role:
        case Role.ADMIN:
            return admin_menu()
        case Role.HEADMAN:
            return headman_menu()
        case Role.VICE_HEADMAN:
            return vice_headman_menu()
        case Role.STUDENT:
            return student_menu()
