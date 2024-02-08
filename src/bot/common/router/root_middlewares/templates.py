import traceback

__all__ = [
    "SOMETHING_WENT_WRONG_TEMPLATE",
    "something_went_wrong_template"
]


def something_went_wrong_template(exception: Exception, user_telegram_id: int) -> str:
    return (f"Произошла ошибка {exception} у пользователя с telegram ID {user_telegram_id}. Возможно, стоит "
            f"предпринять какие-то меры.\n"
            f"{traceback.format_exc()}"
            )


SOMETHING_WENT_WRONG_TEMPLATE = (
    "Что-то пошло не так, попробуйте снова или сообщите администраторам об ошибке в @noheadproblemsbot."
)
