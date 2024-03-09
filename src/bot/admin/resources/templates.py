from src.modules.student_management.domain.models import Group

__all__ = [
    "ADMIN_PANEL_TEMPLATE",
    "users_count_template",
    "group_list_template"
]


ADMIN_PANEL_TEMPLATE = "<b>Выбери необходимую опцию из предложенных ниже:</b>"


def users_count_template(users_count: int) -> str:
    return f"Количество пользователей: {users_count}"


def group_list_template(groups: list[Group]) -> str:  # a logic must be added
    template = "<b>Информация по группам:</b>\n\n"

    for group in groups:
        template += f"Группа <i>{group.name}</i>"

    return template
