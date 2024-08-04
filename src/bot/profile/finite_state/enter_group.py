from collections.abc import Callable, Coroutine
from typing import Any

from aiogram import Bot, F
from aiogram.types import Message, User

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import EnterGroupContext
from src.bot.profile.finite_state.profile_update_states import ProfileUpdateStates
from src.bot.profile.resources.inline_buttons import accept_or_deny_enter_group_buttons, get_back_button
from src.bot.profile.resources.templates import (
    CHOOSE_BUTTONS_ABOVE_TEMPLATE,
    FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    HEADMAN_ALREADY_EXISTS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
    student_send_enter_group_request_template,
)
from src.modules.common.infrastructure.config import ADMIN_IDS
from src.modules.student_management.application.commands import CacheStudentEnterGroupDataCommand
from src.modules.student_management.application.queries import (
    CheckGroupExistsInUniQuery,
    FindGroupByNameAndAliasQuery,
    FindGroupHeadmanQuery,
)
from src.modules.student_management.application.repositories import StudentEnterGroupDTO
from src.modules.student_management.domain import Role, Student
from src.modules.utils.schedule_api.infrastructure.exceptions import ScheduleApiError

__all__ = [
    "include_enter_group_router",
]


enter_group_router = Router(
    must_be_registered=True,
)


def include_enter_group_router(root_router: RootRouter) -> None:
    root_router.include_router(enter_group_router)


@enter_group_router.message(F.text, ProfileUpdateStates.waiting_new_role)
async def new_role_mistake_handler(message: Message) -> None:
    """Works if user send a message instead of tapping on buttons."""
    await message.answer(CHOOSE_BUTTONS_ABOVE_TEMPLATE)


@enter_group_router.message(F.text, ProfileUpdateStates.waiting_new_uni)
async def new_uni_mistake_handler(message: Message) -> None:
    """Works if user send a message instead of tapping on buttons."""
    await message.answer(CHOOSE_BUTTONS_ABOVE_TEMPLATE)


@enter_group_router.message(F.text, ProfileUpdateStates.waiting_new_group)
async def new_group_handler(
        message: Message,
        state: EnterGroupContext,
        student: Student,
        bot: Bot,
        check_group_exists_in_uni_query: CheckGroupExistsInUniQuery,
        find_group_by_name_and_alias_query: FindGroupByNameAndAliasQuery,
        cache_student_enter_group_data_command: CacheStudentEnterGroupDataCommand,
        find_group_headman_query: FindGroupHeadmanQuery,
        inform_admins_about_exception: Callable[
            [Exception, User | None],
            Coroutine[Any, Any, None],
        ],
) -> None:
    if message.text is None:
        return

    group_name = message.text
    university_alias = await state.university_alias

    try:
        group_exists = await check_group_exists_in_uni_query.execute(
            group_name,
            university_alias,
        )
    except ScheduleApiError as e:
        await message.answer(FAILED_TO_CHECK_GROUP_EXISTENCE_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ProfileUpdateStates.waiting_new_group)
        await inform_admins_about_exception(e, message.from_user)
        return

    if not group_exists:
        await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ProfileUpdateStates.waiting_new_group)
        return

    group = await find_group_by_name_and_alias_query.execute(
        group_name,
        await state.university_alias,
    )
    role = await state.role

    # Группа существует, в ней есть староста, а пользователь староста
    if group is not None and role == Role.HEADMAN:
        group_headman = await find_group_headman_query.execute(group.id)
        if group_headman is not None:
            await message.answer(HEADMAN_ALREADY_EXISTS_TEMPLATE)
            await state.set_state(ProfileUpdateStates.waiting_new_group)
            return

    # Группа не существует, а пользователь студент
    if group is None and role == Role.STUDENT:
        await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
        await state.set_state(ProfileUpdateStates.waiting_new_group)
        return

    # Групппа существует, но в ней нет старосты, а пользователь студент
    if group is not None and role == Role.STUDENT:
        group_headman = await find_group_headman_query.execute(group.id)
        if group_headman is None:
            await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
            await state.set_state(ProfileUpdateStates.waiting_new_group)
            return

    await state.set_telegram_id(student.telegram_id)
    await state.set_group_name(group_name)

    match await state.role:
        case Role.STUDENT:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE)
        case Role.HEADMAN:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE)

    student_data = await state.get_data()
    await cache_student_enter_group_data_command.execute(StudentEnterGroupDTO(**student_data))

    role = await state.role

    if role == Role.HEADMAN:
        await state.clear()
        await state.set_state(ProfileUpdateStates.on_verification)
        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                student_send_enter_group_request_template(
                    student.last_name,
                    student.first_name,
                    role,
                    student.telegram_id,
                    message.from_user.username,
                ),
                reply_markup=accept_or_deny_enter_group_buttons(student.telegram_id),
            )
        return

    if group is None:
        raise RuntimeError
    headman = await find_group_headman_query.execute(group.id)

    if headman is None:
        msg = "Group already must have a headman"
        raise RuntimeError(msg)

    await state.clear()
    await state.set_state(ProfileUpdateStates.on_verification)
    await bot.send_message(
        headman.telegram_id,
        student_send_enter_group_request_template(
            student.last_name,
            student.first_name,
            role,
            student.telegram_id,
            message.from_user.username,
        ),
        reply_markup=accept_or_deny_enter_group_buttons(student.telegram_id),
    )

