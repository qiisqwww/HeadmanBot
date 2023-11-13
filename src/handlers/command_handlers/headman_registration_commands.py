from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from asyncpg.pool import Pool
from loguru import logger

from src.config import HEADMAN_PASSWORD
from src.dto.student import Student
from src.resources import (PASS_ASK_MESSAGE,
                           STAROSTA_REG_MESSAGE,
                           WRONG_PASSWORD)
from src.middlewares import (CheckHeadmanMiddleware,
                             CheckRegistrationMiddleware)
from src.resources import (load_void_button,
                           load_headman_buttons)
from src.services import StudentService
from src.states import SetHeadman

__all__ = [
    "headman_registration_router",
]


headman_registration_router = Router()
headman_registration_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=True))
headman_registration_router.message.middleware(CheckHeadmanMiddleware(must_be_headman=False))


@headman_registration_router.message(F.text == "Я староста")
@logger.catch
async def start_headmen(message: Message, state: FSMContext) -> None:
    await message.answer(text=PASS_ASK_MESSAGE,
                         reply_markup=load_void_button())
    logger.trace("set_headman command, password was asked")

    await state.set_state(SetHeadman.get_password)


@headman_registration_router.message(SetHeadman.get_password, F.text)
@logger.catch
async def get_password(message: Message, state: FSMContext, pool: Pool, student: Student) -> None:
    async with pool.acquire() as conn:
        logger.trace("Password for headman registration was handled.")
        if message.text == HEADMAN_PASSWORD:
            student_service = StudentService(conn)
            await student_service.make_headman(student)

            await message.answer(text=STAROSTA_REG_MESSAGE,
                                 reply_markup=load_headman_buttons())
        else:
            await message.answer(WRONG_PASSWORD)

        await state.clear()
