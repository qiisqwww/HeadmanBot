from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from asyncpg.pool import Pool
from loguru import logger

from src.config import HEADMAN_PASSWORD
from src.messages import PASS_ASK_MESSAGE, STAROSTA_REG_MESSAGE, WRONG_PASSWORD
from src.middlewares import CheckHeadmanMiddleware, CheckRegistrationMiddleware
from src.services import StudentService
from src.states import SetHeadman

__all__ = [
    "headman_registration_router",
]


headman_registration_router = Router()
headman_registration_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=True))
headman_registration_router.message.middleware(CheckHeadmanMiddleware(must_be_headman=False))


@headman_registration_router.message(Command("set_headman"))
@logger.catch
async def start_headmen(message: types.Message, state: FSMContext) -> None:
    await message.answer(PASS_ASK_MESSAGE)
    logger.trace("set_headman command, password was asked")

    await state.set_state(SetHeadman.get_password)


@headman_registration_router.message(SetHeadman.get_password, F.text)
@logger.catch
async def get_password(message: types.Message, state: FSMContext, pool: Pool) -> None:
    if message.from_user is None:
        return

    user_id = message.from_user.id
    async with pool.acquire() as conn:
        logger.trace("Password for headman registration was handled.")
        if message.text == HEADMAN_PASSWORD:
            student_service = StudentService(conn)
            await student_service.make_headman(user_id)

            await message.answer(STAROSTA_REG_MESSAGE)
        else:
            await message.answer(WRONG_PASSWORD)

        await state.clear()
