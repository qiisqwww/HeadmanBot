from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import F
from aiogram.types import Message, User

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupContext
from src.bot.change_group.finite_state.change_group_states import ChangeGroupStates
from src.bot.change_group.resources.templates import (
    FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    CHOOSE_NEW_ROLE_TEMPLATE,
    CHOOSE_BUTTONS_ABOVE_TEMPLATE
)
from src.bot.change_group.resources.inline_buttons import get_back_button
from src.modules.student_management.application.queries import (
    CheckGroupExistsInUniQuery,
    FindGroupByNameAndAliasQuery
)
from src.modules.edu_info.application.queries import FetchUniAliasByGroupIdQuery
from src.modules.student_management.domain import Student
from src.modules.utils.schedule_api.infrastructure.exceptions import ScheduleApiError


__all__ = [
    "include_change_group_fsm_router"
]


change_group_fsm_router = Router(
    must_be_registered=True,
)


def include_change_group_fsm_router(root_router: RootRouter) -> None:
    root_router.include_router(change_group_fsm_router)


@change_group_fsm_router.message(F.text, ChangeGroupStates.waiting_new_group)
async def new_group_handler(
        message: Message,
        state: ChangeGroupContext,
        student: Student,
        check_group_exists_in_uni_query: CheckGroupExistsInUniQuery,
        find_group_by_name_and_alias_query: FindGroupByNameAndAliasQuery,
        fetch_uni_alias_by_group_id_query: FetchUniAliasByGroupIdQuery,
        inform_admins_about_exception: Callable[
            [Exception, User | None],
            Coroutine[Any, Any, None],
        ]
) -> None:
    if message.text is None:
        return

    group_name = message.text
    university_alias = await fetch_uni_alias_by_group_id_query.execute(student.group_id)

    try:
        group_exists = await check_group_exists_in_uni_query.execute(
            group_name,
            university_alias
        )
    except ScheduleApiError as e:
        await message.answer(FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ChangeGroupStates.waiting_new_group)
        await inform_admins_about_exception(e, message.from_user)
        return

    if not group_exists:
        await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ChangeGroupStates.waiting_new_group)
        return

    group = await find_group_by_name_and_alias_query.execute(
        group_name,
        university_alias
    )

    await message.answer(CHOOSE_NEW_ROLE_TEMPLATE, reply_markup=role_buttons())

    await state.set_new_group_name(group_name)
    await state.set_university_alias(university_alias)
    await state.set_state(ChangeGroupStates.waiting_new_role)


@change_group_fsm_router.message(F.text, ChangeGroupStates.waiting_new_role)
async def new_role_handler(message: Message) -> None:
    if message.text is None:
        return

    await message.answer(CHOOSE_BUTTONS_ABOVE_TEMPLATE, reply_markup=get_back_button())
