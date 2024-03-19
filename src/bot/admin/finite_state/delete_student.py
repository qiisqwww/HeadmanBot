from aiogram.types import Message

from src.bot.admin.delete_student_states import DeleteStudentStates
from src.bot.admin.resources.templates import (
    GROUP_DOES_NOT_EXIST_TEMPLATE,
    INCORRECT_DATA_ERROR_TEMPLATE,
    ONLY_THREE_FIELDS_TEMPLATE,
    STUDENT_DOES_NOT_EXIST_TEMPLATE,
    STUDENT_WAS_DELETED_TEMPLATE,
)
from src.bot.common import RootRouter, Router
from src.bot.common.contextes import DeleteStudentContext
from src.modules.common.infrastructure import DEBUG
from src.modules.student_management.application.commands import (
    DeleteStudentByFullnameGroupCommand,
    DeleteStudentByTGIDCommand,
)
from src.modules.student_management.application.exceptions import (
    NotFoundGroupError,
    NotFoundStudentError,
)
from src.modules.student_management.domain.enums import Role

__all__ = [
    "include_delete_user_finite_state_router",
]

delete_user_finite_state_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT,
)


def include_delete_user_finite_state_router(root_router: RootRouter) -> None:
    root_router.include_router(delete_user_finite_state_router)


@delete_user_finite_state_router.message(DeleteStudentStates.waiting_telegram_id)
async def ask_student_telegram_id(
    message: Message,
    delete_student_by_tg_id_command: DeleteStudentByTGIDCommand,
    state: DeleteStudentContext,
) -> None:
    if message.text is None or message.from_user is None:
        return

    try:
        telegram_id = int(message.text)
    except ValueError:
        await message.answer(INCORRECT_DATA_ERROR_TEMPLATE)
        await state.set_state(DeleteStudentStates.waiting_telegram_id)
        return

    try:
        await delete_student_by_tg_id_command.execute(telegram_id)
    except NotFoundStudentError:
        await message.answer(STUDENT_DOES_NOT_EXIST_TEMPLATE)
        await state.set_state(DeleteStudentStates.waiting_telegram_id)

        return

    await message.answer(STUDENT_WAS_DELETED_TEMPLATE)

    await state.clear()


@delete_user_finite_state_router.message(DeleteStudentStates.waiting_fullname_group)
async def ask_student_fullname_group_name(
    message: Message,
    delete_student_by_fullname_group_command: DeleteStudentByFullnameGroupCommand,
    state: DeleteStudentContext,
) -> None:
    if message.text is None or message.from_user is None:
        return

    data = message.text.split()
    if len(data) != 3:
        await message.answer(ONLY_THREE_FIELDS_TEMPLATE)

        await state.set_state(DeleteStudentStates.waiting_fullname_group)
        return

    last_name, first_name, group_name = data

    try:
        await delete_student_by_fullname_group_command.execute(
            first_name,
            last_name,
            group_name,
        )
    except NotFoundGroupError:
        await message.answer(GROUP_DOES_NOT_EXIST_TEMPLATE)

        await state.set_state(DeleteStudentStates.waiting_fullname_group)
        return
    except NotFoundStudentError:
        await message.answer(STUDENT_DOES_NOT_EXIST_TEMPLATE)

        await state.set_state(DeleteStudentStates.waiting_fullname_group)
        return

    await message.answer(STUDENT_WAS_DELETED_TEMPLATE)

    await state.clear()
