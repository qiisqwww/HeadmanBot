__all__ = [
    "NO_LESSONS_TODAY_TEMPLATE",
    "schedule_list_template",
]

from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.render_template import render_template
from src.modules.attendance.domain.models.lesson import Lesson

NO_LESSONS_TODAY_TEMPLATE = """
Сегодня нет пар!"""

def schedule_list_template(schedule: list[Lesson], timezone: str) -> str:
    return render_template("""
Расписание:
{% for lesson in schedule | sort(attribute='start_time') -%}
    {{ lesson.name }} {{ convert_time_from_utc(lesson.start_time, timezone).strftime('%H:%M') }}
{% endfor %}""", schedule=schedule, convert_time_from_utc=convert_time_from_utc, timezone=timezone)
