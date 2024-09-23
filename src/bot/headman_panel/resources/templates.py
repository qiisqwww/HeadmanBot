from src.bot.common.render_template import render_template
from src.modules.student_management.domain.models.student import Student

__all__ = [
    "ALL_PAIRS_TEMPLATE",
    "NO_PAIRS_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_TIME_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_DAY_TEMPLATE",
    "YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE",
    "STUDENT_WAS_NOT_FOUND_TEMPLATE",
    "YOU_WAS_DOWNGRADED_TO_STUDENT_TEMPLATE",
    "FAILED_TO_DOWNGRADE_VICEHEADMAN_ROLE_TEMPLATE",
    "CHOOSE_USER_TO_DOWNGRADE_TEMPLATE",
    "CHOOSE_USER_TO_ENHANCE_TEMPLATE",
    "FAILED_TO_GRANT_VICEHEADMAN_ROLE_TEMPLATE",
    "USER_WAS_SUCCESSFULLY_ENHANCED",
    "USER_WAS_SUCCESSFULLY_DOWNGRADED",
]




YOU_CAN_NOT_ANSWER_TIME_TEMPLATE = """
Вы не можете отметиться! Занятия уже начались!"""

YOU_CAN_NOT_ANSWER_DAY_TEMPLATE = """
Вы не можете отметиться за другой день!"""

ALL_PAIRS_TEMPLATE = """
Вы выбрали <b>посетить все пары</b>"""

NO_PAIRS_TEMPLATE = """
Вы выбрали <b>не посещать пары</b>"""


YOU_WAS_GRADED_TO_VICEHEADMAN_TEMPLATE = """Вы были повышены до заместителя старосты.
Вы теперь можете просматривать посещаемость группы. Для просмотра посещаемости нажмите на кнопку "Группа".
"""

YOU_WAS_DOWNGRADED_TO_STUDENT_TEMPLATE = "С вас была снята роль заместителя старосты."

STUDENT_WAS_NOT_FOUND_TEMPLATE = "Пользователь не был найден, попробуйте заново."

FAILED_TO_GRANT_VICEHEADMAN_ROLE_TEMPLATE = (
    'Можно дать роль заместителя старосты только пользователю с ролью "студент".'
)

FAILED_TO_DOWNGRADE_VICEHEADMAN_ROLE_TEMPLATE = (
    'Можно снять роль заместителя старосты только пользователю с ролью "зам старосты".'
)

CHOOSE_USER_TO_DOWNGRADE_TEMPLATE = """
Выберите пользователя, которого хотите понизить до студента."""

CHOOSE_USER_TO_ENHANCE_TEMPLATE = """
Выберите пользователя, которого хотите повысить до зама старосты."""

USER_WAS_SUCCESSFULLY_ENHANCED = """
Пользователю была успешна выдана роль заместителя старосты"""

USER_WAS_SUCCESSFULLY_DOWNGRADED = """
У пользователя была успешна убрана роль зама старосты"""

def students_list(students: list[Student]) -> str:
    return render_template(
        """<b>Список группы</b>

{% for student in students | sort(attribute='fullname') -%}
    {{loop.index}}. <a href="tg://user?id={{ student.telegram_id }}">{{ student.fullname }}</a>
{% endfor %}
""",
        students=students,
    )
