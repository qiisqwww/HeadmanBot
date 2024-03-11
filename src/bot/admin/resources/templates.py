from src.bot.common.render_template import render_template
from src.modules.edu_info.domain.models import GroupAdminInfo

__all__ = [
    "ADMIN_PANEL_TEMPLATE",
    "users_count_template",
    "group_list_template",
]


ADMIN_PANEL_TEMPLATE = "<b>Выбери необходимую опцию из предложенных ниже:</b>"


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

{% endfor %}""",
        groups=groups,
    )
