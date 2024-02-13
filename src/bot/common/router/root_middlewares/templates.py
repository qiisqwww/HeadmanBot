import traceback

from src.bot.common.render_template import render_template

__all__ = [
    "SOMETHING_WENT_WRONG_TEMPLATE",
    "something_went_wrong_template",
]


def something_went_wrong_template(exception: Exception, user_telegram_id: int) -> str:
    return render_template(
        'Произошла ошибка {{exception}} у пользователя с telegram ID <a href="tg://user?id={{ user_telegram_id }}">Пользователь</a>.'
        "Возможно, стоит предпринять какие-то меры.\n"
        "{{traceback.format_exc()}}",
        autoescape=True,
        traceback=traceback,
        exception=exception,
        user_telegram_id=user_telegram_id,
    )


SOMETHING_WENT_WRONG_TEMPLATE = "Что-то пошло не так, попробуйте снова или сообщите администраторам об ошибке в @noheadproblemsbot."
