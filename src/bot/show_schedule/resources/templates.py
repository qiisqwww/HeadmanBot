__all__ = [
    "NO_LESSONS_TODAY_TEMPLATE",
    "schedule_list_template",
]

from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.render_template import render_template
from src.modules.utils.schedule_api.domain.schedule import Schedule

NO_LESSONS_TODAY_TEMPLATE = """
Сегодня нет пар!"""


def schedule_list_template(schedule: list[Schedule], timezone: str, day: str) -> str:
    return render_template(
        """
Расписание на {{day}}:

{% for lesson in schedule | sort(attribute='start_time') -%}
    {{ convert_time_from_utc(lesson.start_time, timezone).strftime('%H:%M') }} {{ lesson.lesson_name }} {{ lesson.classroom }}
{% endfor %}""",
        schedule=schedule,
        convert_time_from_utc=convert_time_from_utc,
        timezone=timezone,
        day=day,
    )
