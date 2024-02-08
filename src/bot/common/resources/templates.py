from jinja2 import Template

__all__ = [
    "your_choice_is_template"
]


def your_choice_is_template(is_fullname_correct: bool) -> str:
    template = Template(
        "Вы выбрали {% if is_fullname_correct %} '<b>да</b>' {% else %} '<b>нет</b>' {% endif %}",
        autoescape=True,
    )
    return template.render(is_fullname_correct=is_fullname_correct)
