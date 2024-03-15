from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import DeleteUserContext
from src.bot.admin.delete_student_states import DeleteStudentStates
from src.bot.admin.resources.templates import (
    STUDENT_WAS_DELETED_TEMPLATE,
    STUDENT_DOES_NOT_EXIST_TEMPLATE
)
from src.modules.student_management.application.commands import (
    DeleteUserByTGIDCommand,
    NotFoundStudentError
)
from src.modules.student_management.domain.enums import Role
from src.modules.common.infrastructure import DEBUG

__all__ = [
    "include_delete_user_finite_state_router",
]

delete_user_finite_state_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT
)


def include_delete_user_finite_state_router(root_router: RootRouter) -> None:
    root_router.include_router(delete_user_finite_state_router)


@delete_user_finite_state_router.message(DeleteStudentStates.waiting_telegram_id)
async def ask_student_telegram_id(
        message: Message,
        delete_user_by_tg_id_command: DeleteUserByTGIDCommand,
        state: DeleteUserContext,
) -> None:
    if message is None or message.from_user is None:
        return

    try:
        await delete_user_by_tg_id_command.execute(int(message.text))
    except NotFoundStudentError:
        await message.answer(STUDENT_WAS_DELETED_TEMPLATE)
        await state.set_state(DeleteStudentStates.waiting_telegram_id)

        return

    await message.answer(STUDENT_WAS_DELETED_TEMPLATE)

    await state.clear()


@delete_user_finite_state_router.message(DeleteStudentStates.waiting_fullname_group)
async def ask_student_fullname_group_name(
        message: Message,
        state: DeleteUserContext
) -> None:
    if message is None or message.from_user is None:
        return

    await state.clear()
