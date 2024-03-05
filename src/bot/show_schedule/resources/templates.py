__all__ = [
    "NO_LESSONS_TODAY_TEMPLATE",
    "schedule_list_template",
]


from datetime import datetime, time, timedelta

from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.render_template import render_template
from src.modules.utils.schedule_api.domain.schedule import Schedule

NO_LESSONS_TODAY_TEMPLATE = """
Сегодня нет пар!"""


def get_name_of_day(weekday: int) -> str:
    match weekday:
        case 0:
            return "понедельник"
        case 1:
            return "вторник"
        case 2:
            return "среда"
        case 3:
            return "четверг"
        case 4:
            return "пятница"
        case 5:
            return "суббота"
        case 6:
            return "воскресенье"
        case _:
            pass


def end_time(start_time: time, timezone: str) -> time:
    end_time_sum = datetime(
        day=1,
        month=1,
        year=1,
        hour=start_time.hour,
        minute=start_time.minute,
        tzinfo=start_time.tzinfo,
    ) + timedelta(
        hours=1,
        minutes=30,
    )
    return convert_time_from_utc(
        end_time_sum.time(),
        timezone,
    )


def schedule_list_template(
    schedule: list[Schedule],
    timezone: str,
    day: str,
    weekday: int,
    has_classrooms: bool,
) -> str:
    return render_template(
        """
Расписание на {{day}} ({{day_of_week}}):

{% for lesson in schedule | sort(attribute='start_time') -%}
    Пара {{ loop.index }} {{ convert_time_from_utc(lesson.start_time, timezone).strftime('%H:%M')}}-{{end_time(lesson.start_time, timezone).strftime('%H:%M') }} {% if has_classrooms %}в <em>{{ lesson.classroom }}</em>{% endif %}\n
<b>{{ lesson.lesson_name }}</b>

{% endfor %}""",
        schedule=schedule,
        convert_time_from_utc=convert_time_from_utc,
        end_time=end_time,
        timezone=timezone,
        day=day,
        day_of_week=get_name_of_day(weekday),
        has_classrooms=has_classrooms,
    )
