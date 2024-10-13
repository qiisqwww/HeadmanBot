import traceback

from aiogram.types import User
from jinja2 import Template

__all__ = [
    "something_went_wrong_for_admin_template",
    "something_went_wrong_for_admin_in_job_template",
]


def something_went_wrong_for_admin_template(
    exception: Exception,
    user: User | None,
) -> str:
    return Template(
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
        autoescape=True,
        trim_blocks=True,
    ).render(
        traceback=traceback,
        exception=exception,
        user=user,
    )


def something_went_wrong_for_admin_in_job_template(
    exception: Exception,
    job_name: str,
) -> str:
    return Template(
        """Произошла ошибка <b>{{exception}}</b> в фоновой задаче {{ job_name }}.
Возможно, стоит предпринять какие-то меры.
{{traceback.format_exc()}}
""",
        autoescape=True,
        trim_blocks=True,
    ).render(
        traceback=traceback,
        exception=exception,
        job_name=job_name,
    )
