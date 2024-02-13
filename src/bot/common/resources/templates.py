import traceback

from aiogram.types import User

from src.bot.common.render_template import render_template

__all__ = [
    "your_choice_is_template",
    "SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE",
    "something_went_wrong_for_admin_in_job_template",
    "something_went_wrong_for_admin_template",
]


def your_choice_is_template(is_fullname_correct: bool) -> str:
    return render_template(
        "Вы выбрали {% if is_fullname_correct %} '<b>да</b>' {% else %} '<b>нет</b>' {% endif %}",
        is_fullname_correct=is_fullname_correct,
    )


def something_went_wrong_for_admin_template(
    exception: Exception,
    user: User | None,
) -> str:
    return render_template(
        """Произошла ошибка <b>{{exception}}</b> у {% if user is none -%}
    пользователя.
{% elif user.username is none -%}
    <a href='tg://user?id={{ user.telegram_id }}'>пользователя</a>.
{% else -%}
    @{{ user.username }}.
{% endif %}
Возможно, стоит предпринять какие-то меры.
{{traceback.format_exc()}}
""",
        traceback=traceback,
        exception=exception,
        user=user,
    )


def something_went_wrong_for_admin_in_job_template(
    exception: Exception,
    job_name: str,
) -> str:
    return render_template(
        """Произошла ошибка <b>{{exception}}</b> в фоновой задаче {{ job_name }}.
Возможно, стоит предпринять какие-то меры.
{{traceback.format_exc()}}
""",
        traceback=traceback,
        exception=exception,
        job_name=job_name,
    )


SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE = "Что-то пошло не так, попробуйте снова или сообщите администраторам об ошибке в @noheadproblemsbot."
