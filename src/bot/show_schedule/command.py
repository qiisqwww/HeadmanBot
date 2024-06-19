from aiogram.types import Message

from src.bot.common import CommandFilter, RootRouter, Router, TelegramCommand
from src.bot.show_schedule.resources import (
    show_choose_period_buttons,
    CHOOSE_SCHEDULE_PERIOD_TEMPLATE
)

__all__ = [
    "include_get_schedule_command",
]


get_schedule_command_router = Router(
    must_be_registered=True,
)


def include_get_schedule_command(root_router: RootRouter) -> None:
    root_router.include_router(get_schedule_command_router)


@get_schedule_command_router.message(CommandFilter(TelegramCommand.SHOW_SCHEDULE))
async def get_attendance_command(message: Message) -> None:
    await message.answer(
        CHOOSE_SCHEDULE_PERIOD_TEMPLATE,
        reply_markup=show_choose_period_buttons()
    )
