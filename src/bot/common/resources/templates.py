from src.bot.common.render_template import render_template

__all__ = [
    "your_choice_is_template",
    "SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE",
]


def your_choice_is_template(is_fullname_correct: bool) -> str:
    return render_template(
        "Вы выбрали {% if is_fullname_correct %} '<b>да</b>' {% else %} '<b>нет</b>' {% endif %}",
        is_fullname_correct=is_fullname_correct,
    )


SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE = """Что-то пошло не так.
Попробуйте снова или сообщите администраторам об ошибке в @noheadproblemsbot."""
