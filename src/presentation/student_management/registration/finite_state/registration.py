from aiogram import F
from aiogram.types import Message

from src.application.student_management.queries import CheckGroupExistsInUniQuery

# from src.external.apis.schedule_api.exceptions import FailedToCheckGroupExistence
from src.presentation.common.router import Router

from ..registration_context import RegistrationContext
from ..registration_states import RegistrationStates
from ..resources.templates import (
    ASK_BIRTHDATE_TEMPLATE,
    GROUP_DOESNT_EXISTS_TEMPLATE,
    INCORRECT_STUDENT_ROLE_TEMPLATE,
    INCORRECT_UNIVERSITY_TEMPLATE,
)

__all__ = [
    "registration_finite_state_router",
]

registration_finite_state_router = Router(
    must_be_registered=False,
)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_role)
async def incorrect_student_role(message: Message) -> None:
    await message.answer(INCORRECT_STUDENT_ROLE_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_university)
async def incorrect_university(message: Message) -> None:
    await message.answer(INCORRECT_UNIVERSITY_TEMPLATE)


@registration_finite_state_router.message(F.text, RegistrationStates.waiting_group)
async def handling_group(
    message: Message,
    state: RegistrationContext,
    check_group_exists_in_uni_query: CheckGroupExistsInUniQuery,
) -> None:
    if message.text is None:
        return

    try:
        group_exists = await check_group_exists_in_uni_query.execute(message.text, await state.university_alias)
        if not group_exists:
            await message.answer(GROUP_DOESNT_EXISTS_TEMPLATE)
            await state.set_state(RegistrationStates.waiting_group)
            return
    except Exception:
        await message.answer(
            "Не удалось проверить наличие группы в университете, попробуйте снова или напишите в @noheadproblemsbot"
        )
        await state.set_state(RegistrationStates.waiting_group)
        return

    # group = await group_service.find_by_name_and_uni(message.text, await state.university_alias)
    # if await state.role == Role.STUDENT and group is None:
    #     await message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE)
    #     await state.set_state(RegistrationStates.waiting_group)
    #     return
    #
    # if (
    #     group is not None
    #     and await state.role == Role.HEADMAN
    #     and await student_service.get_headman_by_group_name(group.name) is not None
    # ):
    #     await message.answer(HEADMAN_ALREADY_EXISTS_TEMPLATE)
    #     await state.set_state(RegistrationStates.waiting_group)
    #     return
    #
    await state.set_group_name(message.text)
    await message.answer(ASK_BIRTHDATE_TEMPLATE)
    await state.set_state(RegistrationStates.waiting_birthdate)


# @registration_finite_state_router.message(F.text, RegistrationStates.waiting_birthdate)
#
# async def handling_birthmonth(message: Message, state: RegistrationContext) -> None:
#     if message.text is None:
#         return
#
#     if message.text == "0":
#         await state.set_birthday(None)
#     else:
#         try:
#             day, month, year = map(int, message.text.split("."))
#             birthdate = date(year=year, month=month, day=day)
#             await state.set_birthday(birthdate)
#         except Exception:
#             await message.answer(BIRTHDATE_INCORRECT_TEMPLATE)
#             await state.set_state(RegistrationStates.waiting_birthdate)
#             return
#
#     await state.set_state(RegistrationStates.waiting_surname)
#     await message.answer(ASK_SURNAME_TEMPLATE)
#
#
# @registration_finite_state_router.message(F.text, RegistrationStates.waiting_surname)
#
# async def handling_surname(message: Message, state: RegistrationContext) -> None:
#     if message.text is None:
#         return
#
#     if not is_valid_surname_len(message.text):
#         await message.answer(TOO_MUCH_SURNAME_LENGTH_TEMPLATE)
#         await state.set_state(RegistrationStates.waiting_surname)
#         return
#
#     await state.set_surname(message.text)
#     await state.set_state(RegistrationStates.waiting_name)
#     await message.answer(ASK_NAME_TEMPLATE)
#
#
# @registration_finite_state_router.message(F.text, RegistrationStates.waiting_name)
#
# async def handling_name(
#     message: Message,
#     state: RegistrationContext,
# ) -> None:
#     if message.from_user is None:
#         return
#
#     if message.text is None:
#         return
#
#     if not is_valid_name_len(message.text):
#         await message.answer(TOO_MUCH_NAME_LENGTH_TEMPLATE)
#         await state.set_state(RegistrationStates.waiting_name)
#         return
#
#     await state.set_name(message.text)
#
#     await message.answer(
#         asking_fullname_validation_template(await state.surname, await state.name),
#         reply_markup=ask_fullname_validity_buttons(),
#     )
