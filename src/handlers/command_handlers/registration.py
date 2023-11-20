from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from asyncpg.pool import Pool
from loguru import logger

from src.buttons import (
    role_buttons,
    university_list_buttons,
    start_button)
from src.reg_states import RegistrationStates
from src.messages import (
    START_MESSAGE,
    GROUP_DOESNT_EXISTS_MESSAGE,
    ASK_GROUP_MESSAGE,
    HEADMAN_OR_STUDENT_MESSAGE,
    YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE,
    INCORRECT_DATA_MESSAGE,
    ASK_SURNAME_MESSAGE,
    ASK_NAME_MESSAGE,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_MESSAGE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_MESSAGE
)
from src.services import GroupService
from src.enums import UniversityId
from src.api import ScheduleApi
from src.handlers.command_handlers.verification_poll import verify_registration
from src.buttons import remove_reply_buttons
from src.middlewares import CheckRegistrationMiddleware


registration_router = Router()
registration_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=False))


@registration_router.message(Command("start"))
@logger.catch
async def start_command(message: Message, state: FSMContext) -> None:
    await message.answer(text=START_MESSAGE,
                         reply_markup=university_list_buttons())
    await state.set_state(RegistrationStates.waiting_university)


@registration_router.message(F.text, RegistrationStates.waiting_university)
@logger.catch
async def handling_university(message: Message, state: FSMContext) -> None:
    """must be added a verification for university's existence"""
    await message.answer(text=ASK_GROUP_MESSAGE,
                         reply_markup=remove_reply_buttons())

    #await state.update_data(university=message.text)
    await state.set_state(RegistrationStates.waiting_group)


@registration_router.message(F.text, RegistrationStates.waiting_group)
@logger.catch
async def handling_group(message: Message, state: FSMContext) -> None:
    """now we only check MIREA groups"""
    api = ScheduleApi(UniversityId.MIREA)
    if not await api.group_exists(message.text):
        await message.answer(GROUP_DOESNT_EXISTS_MESSAGE)
        await state.set_state(RegistrationStates.waiting_group)
        return

    await state.update_data(group_name=message.text)
    await message.answer(text=HEADMAN_OR_STUDENT_MESSAGE,
                         reply_markup=role_buttons())
    await state.set_state(RegistrationStates.waiting_role)


@registration_router.message(F.text, RegistrationStates.waiting_role)
@logger.catch
async def handling_role(message: Message, state: FSMContext, pool: Pool) -> None:
    match message.text:
        case "Я староста":
            await state.update_data(is_headman="true")
        case "Я студент":
            async with pool.acquire() as con:
                data = await state.get_data()
                group_service = GroupService(con)
                group = await group_service.get_by_name(data["group_name"])
                if group is None:
                    await message.answer(
                        text=YOUR_GROUP_IS_NOT_REGISTERED_MESSAGE,
                        reply_markup=start_button())
                    await state.clear()
                    return
            await state.update_data(is_headman="false")
        case _:
            await message.answer(INCORRECT_DATA_MESSAGE)
            await state.set_state(RegistrationStates.waiting_role)
            return

    await message.answer(text=ASK_SURNAME_MESSAGE,
                         reply_markup=remove_reply_buttons())
    await state.set_state(RegistrationStates.waiting_surname)


@registration_router.message(F.text, RegistrationStates.waiting_surname)
@logger.catch
async def handling_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)

    await message.answer(text=ASK_NAME_MESSAGE)
    await state.set_state(RegistrationStates.waiting_name)


@registration_router.message(F.text, RegistrationStates.waiting_name)
@logger.catch
async def handling_name(message: Message, state: FSMContext, pool: Pool):
    await state.update_data(name=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    await state.set_state(RegistrationStates.on_verification)

    data = await state.get_data()
    if data["is_headman"] == "true":
        await message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_MESSAGE)
        await verify_registration(user_id=message.from_user.id, state=state, pool=pool)
        return

    await message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_MESSAGE)
    await verify_registration(user_id=message.from_user.id, state=state, pool=pool)
