from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.kernel.config import ADMIN_IDS
from src.kernel.external.apis import ScheduleApi
from src.kernel.role import Role
from src.modules.student.internal.controllers.unregistred.registration_context import (
    RegistrationContext,
)
from src.modules.student.internal.controllers.unregistred.registration_states import (
    RegistrationStates,
)
from src.modules.student.internal.gateways.group_gateway import GroupGateway
from src.modules.student.internal.resources.buttons.inline_buttons import (
    accept_or_deny_buttons,
)
from src.modules.student.internal.resources.templates import (
    ASK_BIRTHMONTH_TEMPLATE,
    ASK_NAME_TEMPLATE,
    ASK_SURNAME_TEMPLATE,
    GROUP_ALREADY_EXISTS_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    INCORRECT_STUDENT_ROLE_TEMPLATE,
    INCORRECT_UNIVERSITY_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
)
from src.modules.student.internal.services import CacheStudentService, StudentService

__all__ = [
    "registration_finite_state_router",
]

registration_finite_state_router = Router(
    must_be_registered=False,
    services={
        "group_gateway": GroupGateway,
        "cache_student_service": CacheStudentService,
        "student_service": StudentService,
    },
)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_role)
@logger.catch
async def incorrect_student_role(message: Message) -> None:
    await message.answer(INCORRECT_STUDENT_ROLE_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_university)
@logger.catch
async def incorrect_university(message: Message) -> None:
    await message.answer(INCORRECT_UNIVERSITY_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_group)
@logger.catch
async def handling_group(message: Message, state: FSMContext, group_gateway: GroupGateway) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    api = ScheduleApi(await registration_ctx.university_alias)

    if not await api.group_exists(message.text):
        await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE)
        await registration_ctx.set_state(RegistrationStates.waiting_group)
        return

    group = await group_gateway.find_group_by_name_and_uni(message.text, await registration_ctx.university_alias)

    if await registration_ctx.role == Role.HEADMAN and group is not None:
        await message.answer(GROUP_ALREADY_EXISTS_TEMPLATE)
        await registration_ctx.set_state(RegistrationStates.waiting_group)
        return

    if await registration_ctx.role == Role.STUDENT and group is not None:
        await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
        await registration_ctx.set_state(RegistrationStates.waiting_group)
        return

    await registration_ctx.set_group_name(message.text)
    await message.answer(ASK_BIRTHMONTH_TEMPLATE)
    await registration_ctx.set_state(RegistrationStates.waiting_birthdate)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_birthdate)
@logger.catch
async def handling_birthmonth(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    await registration_ctx.set_birthday(None)

    # if 1 <= birthmonth <= 12:
    #     await registration_ctx.set_birthmonth(birthmonth)
    #     await message.answer(ASK_BIRTHDAY_TEMPLATE)
    #     await registration_ctx.set_state(RegistrationStates.waiting_birthday)
    # elif birthmonth == 0:
    #     await registration_ctx.set_birthmonth(0)
    #     await registration_ctx.set_birthday(0)
    #     await registration_ctx.set_state(RegistrationStates.waiting_surname)
    #     await message.answer(ASK_SURNAME_TEMPLATE)
    # else:
    #     await message.answer(BIRTHMONTH_INCORRECT_TEMPLATE)
    #     await registration_ctx.set_state(RegistrationStates.waiting_birthmonth)

    await registration_ctx.set_state(RegistrationStates.waiting_surname)
    await message.answer(ASK_SURNAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_surname)
@logger.catch
async def handling_surname(message: Message, state: FSMContext) -> None:
    registration_ctx = RegistrationContext(state)

    if message.text is None:
        return

    await registration_ctx.set_surname(message.text)
    await registration_ctx.set_state(RegistrationStates.waiting_name)
    await message.answer(ASK_NAME_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_name)
@logger.catch
async def handling_name(
    message: Message,
    state: FSMContext,
    bot: Bot,
    cache_student_service: CacheStudentService,
    student_service: StudentService,
) -> None:
    registration_ctx = RegistrationContext(state)

    if message.from_user is None:
        return

    if message.text is None:
        return

    await registration_ctx.set_name(message.text)
    await registration_ctx.set_telegram_id(message.from_user.id)
    await registration_ctx.set_state(RegistrationStates.on_verification)

    match await registration_ctx.role:
        case Role.STUDENT:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE)
        case Role.HEADMAN:
            await message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE)

    student_data = await registration_ctx.get_data()
    student_id = await registration_ctx.telegram_id
    await cache_student_service.cache_student(student_data)

    if await registration_ctx.role == Role.HEADMAN:
        surname = await registration_ctx.surname
        name = await registration_ctx.name

        for admin_id in ADMIN_IDS:
            await bot.send_message(
                admin_id,
                f"Староста {surname} {name} подал заявку на регистарцию в боте.",
                reply_markup=accept_or_deny_buttons(student_id),
            )
        return

    headman = [
        student
        for student in await student_service.filter_by_group_name(await registration_ctx.group_name)
        if student.is_headman()
    ][0]

    await bot.send_message(
        headman.telegram_id,
        f"Студент {student_data['surname']} {student_data['name']} подал заявку на регистарцию в вашу группу",
        reply_markup=accept_or_deny_buttons(student_id),
    )

    await state.clear()
