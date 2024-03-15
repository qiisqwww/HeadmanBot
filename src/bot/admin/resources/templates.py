from src.bot.common.render_template import render_template
from src.modules.edu_info.domain.models import GroupAdminInfo

__all__ = [
    "ADMIN_PANEL_TEMPLATE",
    "DELETE_USER_CHOICE_TEMPLATE",
    "INPUT_USER_TG_ID_TEMPLATE",
    "INPUT_FULLNAME_GROUP_TEMPLATE",
    "users_count_template",
    "group_list_template",
]


ADMIN_PANEL_TEMPLATE = "<b>Выбери необходимую опцию из предложенных ниже:</b>"

DELETE_USER_CHOICE_TEMPLATE = "Каким способом нужно удалить пользователя?"

INPUT_USER_TG_ID_TEMPLATE = "Отправь telegram ID пользователя"

INPUT_FULLNAME_GROUP_TEMPLATE = "Отправь Фамилию, Имя и Название группы пользователя через пробел"


def users_count_template(users_count: int) -> str:
    return render_template(
        """Количество пользователей: {{users_count}}""",
        users_count=users_count,
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
