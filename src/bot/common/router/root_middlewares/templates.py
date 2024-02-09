import traceback

from jinja2 import Template

__all__ = [
    "SOMETHING_WENT_WRONG_TEMPLATE",
    "something_went_wrong_template"
]


def something_went_wrong_template(exception: Exception, user_telegram_id: int) -> str:
    template = Template('Произошла ошибка {{exception}} у пользователя с telegram ID <a href="tg://user?id={{ user_telegram_id }}">Пользователь</a>. (ID = user_telegram_id)'
                        'Возможно, стоит предпринять какие-то меры.\n'
                        '{{traceback.format_exc()}}[',
                        autoescape=True)
    return template.render(exception=exception, user_telegram_id=user_telegram_id, traceback=traceback)


SOMETHING_WENT_WRONG_TEMPLATE = (
    "Что-то пошло не так, попробуйте снова или сообщите администраторам об ошибке в @noheadproblemsbot."
)
