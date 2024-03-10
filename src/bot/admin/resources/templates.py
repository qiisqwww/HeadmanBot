from src.modules.edu_info.domain.models import GroupAdminInfo
from src.bot.common.render_template import render_template

__all__ = [
    "ADMIN_PANEL_TEMPLATE",
    "users_count_template",
    "group_list_template"
]


ADMIN_PANEL_TEMPLATE = "<b>Выбери необходимую опцию из предложенных ниже:</b>"


def users_count_template(users_count: int) -> str:
    return render_template(
        """Количество пользователей: {{users_count}}""",
        users_count=users_count
    )


def group_list_template(groups: list[GroupAdminInfo]) -> str:
    return render_template(
        """<b>Информация по группам:</b>
        
{% for group in groups -%}
Группа <i>{{group.name}}</i>
Староста <i><a href="tg://user?id={{ group.headman_first_name }}">{{ group.headman_last_name }}</a></i>

{% endfor %}""",
        groups=groups
    )
