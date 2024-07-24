from datetime import date, timedelta
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.show_schedule.callback_data import (
    ScheduleWeekCallbackData,
    ScheduleDateCallbackData,
    BackToWeekChoiceListCallbackData,
    ScheduleCertainDayCallbackData
)
from src.modules.common.domain import UniversityAlias

__all__ = [
    "show_choose_period_buttons",
    "show_choose_day_buttons",
    "show_get_back_button"
]


def get_short_name_of_day(weekday: int) -> str:
    match weekday:
        case 0:
            return "ПН"
        case 1:
            return "ВТ"
        case 2:
            return "СР"
        case 3:
            return "ЧТ"
        case 4:
            return "ПТ"
        case 5:
            return "СБ"
        case 6:
            return "ВС"
        case _:
            pass


def show_choose_period_buttons(uni: UniversityAlias) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Сегодня", callback_data=ScheduleDateCallbackData(
        chosen_day=date.today(),
        weeks_to_add=0
    ))
    builder.button(text="Текущая неделя", callback_data=ScheduleWeekCallbackData(weeks_to_add=0))
    builder.button(text="Следующая неделя", callback_data=ScheduleWeekCallbackData(weeks_to_add=1))
    builder.button(text="Неделя после следующей", callback_data=ScheduleWeekCallbackData(weeks_to_add=2))
    builder.button(text="Ввести дату вручную", callback_data=ScheduleCertainDayCallbackData())
    builder.button(text="Карта РТУ МИРЭА", url="https://map.mirea.ru/") if uni == UniversityAlias.MIREA else ...

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def show_choose_day_buttons(weeks_to_add: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    day_of_week = date.today() + timedelta(days=7*weeks_to_add)
    week_runner = day_of_week - timedelta(days=day_of_week.weekday() % 7)
    for i in range(7):
        builder.button(
            text=get_short_name_of_day(i) + " | " + str(week_runner),
            callback_data=ScheduleDateCallbackData(
                chosen_day=week_runner,
                weeks_to_add=weeks_to_add
            )
        )
        week_runner = week_runner + timedelta(days=1)
    builder.button(text="← Вернуться назад", callback_data=BackToWeekChoiceListCallbackData())

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def show_get_back_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="← Вернуться назад", callback_data=BackToWeekChoiceListCallbackData())
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
