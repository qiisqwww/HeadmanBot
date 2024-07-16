__all__ = [
    "CHANGE_OR_QUIT_TEMPLATE",
    "ACTION_CANCELLED_TEMPLATE",
    "INPUT_NEW_GROUP_TEMPLATE",
    "YOU_LEFT_GROUP_TEMPLATE",
    "FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE",
    "GROUP_DOESNT_EXISTS_TEMPLATE",
    "GROUP_DOESNT_REGISTERED_TEMPLATE",
    "HEADMAN_ALREADY_EXISTS_TEMPLATE",
    "CHOOSE_NEW_ROLE_TEMPLATE",
    "CHOOSE_BUTTONS_ABOVE_TEMPLATE"
]


CHANGE_OR_QUIT_TEMPLATE = "Вы желаете изменить группу или выйти из текущей?"

ACTION_CANCELLED_TEMPLATE = "Действие отменено"

INPUT_NEW_GROUP_TEMPLATE = "Введите название вашей новой группы"

YOU_LEFT_GROUP_TEMPLATE = "Вы вышли из текущей группы"

FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE = (
    "Не удалось проверить наличие группы в университете, " "попробуйте снова или напишите в @noheadproblemsbot."
)

GROUP_DOESNT_EXISTS_TEMPLATE = (
    "В вашем университете такой группы нет. Попробуйте ввести группу заново, используя заглавные буквы"
)

GROUP_DOESNT_REGISTERED_TEMPLATE = """Группа еще не зарегистрирована в боте.
Попросите своего старосту зарегестрироваться, или введите название группы заново."""

HEADMAN_ALREADY_EXISTS_TEMPLATE = "У выбранной группы уже есть староста. Введите название группы заново."

CHOOSE_NEW_ROLE_TEMPLATE = "Вы староста или студент?"

CHOOSE_BUTTONS_ABOVE_TEMPLATE = "Выберите одну из кнопок в сообщении выше, чтобы выбрать роль."
