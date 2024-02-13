from src.bot.common.render_template import render_template

__all__ = [
    "your_choice_is_template",
]


def your_choice_is_template(is_fullname_correct: bool) -> str:
    return render_template(
        "Вы выбрали {% if is_fullname_correct %} '<b>да</b>' {% else %} '<b>нет</b>' {% endif %}",
        is_fullname_correct=is_fullname_correct,
    )
