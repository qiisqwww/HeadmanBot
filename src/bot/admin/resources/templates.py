from src.bot.common.render_template import render_template
from src.modules.edu_info.domain.models import GroupAdminInfo

__all__ = [
    "ADMIN_PANEL_TEMPLATE",
    "DELETE_STUDENT_CHOICE_TEMPLATE",
    "INPUT_STUDENT_TG_ID_TEMPLATE",
    "INPUT_FULLNAME_GROUP_TEMPLATE",
    "STUDENT_WAS_DELETED_TEMPLATE",
    "STUDENT_DOES_NOT_EXIST_TEMPLATE",
    "GROUP_DOES_NOT_EXIST_TEMPLATE",
    "ONLY_THREE_FIELDS_TEMPLATE",
    "users_count_template",
    "group_list_template",
]


ADMIN_PANEL_TEMPLATE = "<b>Выбери необходимую опцию из предложенных ниже:</b>"

DELETE_STUDENT_CHOICE_TEMPLATE = "Каким способом нужно удалить студента?"

INPUT_STUDENT_TG_ID_TEMPLATE = "Отправь telegram ID студента"

INPUT_FULLNAME_GROUP_TEMPLATE = "Отправь Фамилию, Имя и Название группы студента через пробел"

STUDENT_WAS_DELETED_TEMPLATE = "Студент был успешно удален"

STUDENT_DOES_NOT_EXIST_TEMPLATE = "Пользователя с такими данными не существует. Попробуй еще раз"

GROUP_DOES_NOT_EXIST_TEMPLATE = "В боте не зарегестрировано студента с ввеенной группой. Попробуй еще раз"

ONLY_THREE_FIELDS_TEMPLATE = "Нужно ввести только 3 значения: Фамилию, Имя и Название группы ЧЕРЕЗ ПРОБЕЛ"


def users_count_template(students_count: int) -> str:
    return render_template(
        """Количество студентов: {{students_count}}""",
        students_count=students_count,
    )


def group_list_template(groups: list[GroupAdminInfo]) -> str:
    return render_template(
        """<b>Информация по группам:</b>

{% for group in groups | sort(attribute='name') -%}
Группа <i>{{group.name}}</i>
Староста <i><a href="tg://user?id={{ group.headman_telegram_id }}">{{ group.headman_last_name }} {{ group.headman_first_name }}</a></i>
Telegram ID старосты: {{ group.headman_telegram_id }}

{% endfor %}""",
        groups=groups,
    )
