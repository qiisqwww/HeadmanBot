from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import F
from aiogram.types import Message, User, CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupContext
from src.bot.change_group.finite_state.change_group_states import ChangeGroupStates
from src.bot.change_group.resources.templates import (
    FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    HEADMAN_ALREADY_EXISTS_TEMPLATE,
    CHOOSE_NEW_ROLE_TEMPLATE,
    CHOOSE_BUTTONS_ABOVE_TEMPLATE
)
from src.bot.change_group.resources.inline_buttons import (
    get_back_button,
    role_buttons
)
from src.bot.change_group.callback_data import ChooseRoleCallbackData
from src.modules.student_management.application.queries import (
    CheckGroupExistsInUniQuery,
    FindGroupByNameAndAliasQuery,
    FindGroupHeadmanQuery,
)
from src.modules.edu_info.application.queries import FetchUniAliasByGroupIdQuery
from src.modules.student_management.domain import Role, Student
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


# FOR CALLBACK
@change_group_fsm_router.callback_query(ChooseRoleCallbackData.filter())
async def new_role_handler(
        callback: CallbackQuery,
        callback_data: ChooseRoleCallbackData,
        state: ChangeGroupContext,
        find_group_headman_query: FindGroupHeadmanQuery,
        find_group_by_name_and_alias_query: FindGroupByNameAndAliasQuery,
) -> None:
    if callback_data.role == Role.STUDENT and await state.new_group_name is None:
        await callback.message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ChangeGroupStates.waiting_new_group)
        return

    group = await find_group_by_name_and_alias_query.execute(
        await state.new_group_name,
        await state.university_alias,
    )

    if state.new_group_name is not None and callback_data.role == Role.HEADMAN:
        group_headman = await find_group_headman_query.execute(group.id)
        if group_headman is not None:
            await callback.message.answer(HEADMAN_ALREADY_EXISTS_TEMPLATE, reply_markup=get_back_button())
            await state.set_state(ChangeGroupStates.waiting_new_group)
            return

    await state.clear()
