__all__ = [
    "ADMIN_PANEL_TEMPLATE",
    "users_count_template",
    "group_list_template"
]

ADMIN_PANEL_TEMPLATE = "<b>Выбери необходимую опцию из предложенных ниже:</b>"


def users_count_template(users_count: int) -> str:
    return f"Количество пользователей: {users_count}"


def group_list_template() -> str:  # a logic must be added
    return "<b>Информация по группам:</b>"
