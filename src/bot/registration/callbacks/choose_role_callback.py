from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import RegistrationContext
from src.bot.common.resources import void_inline_buttons
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.registration.callback_data import ChooseRoleCallbackData
from src.bot.registration.finite_state.registration_states import RegistrationStates
from src.bot.registration.resources.inline_buttons import university_list_buttons
from src.bot.registration.resources.templates import (
    ASK_UNIVERSITY_TEMPLATE,
    successful_role_choose_template,
)
from src.modules.student_management.application.queries import GetAllUniversitiesQuery

__all__ = [
    "include_choose_role_router",
]

choose_role_router = Router()


def include_choose_role_router(root_router: RootRouter) -> None:
    root_router.include_router(choose_role_router)


@choose_role_router.callback_query(ChooseRoleCallbackData.filter())
async def get_role_from_user(
    callback: CallbackQuery,
    callback_data: ChooseRoleCallbackData,
    state: RegistrationContext,
    get_all_universities_query: GetAllUniversitiesQuery,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await state.set_role(callback_data.role)

    await safe_message_edit(
        callback,
        successful_role_choose_template(await state.role),
        reply_markup=void_inline_buttons(),
    )

    universities = await get_all_universities_query.execute()

    await callback.message.answer(ASK_UNIVERSITY_TEMPLATE, reply_markup=university_list_buttons(universities))

    await state.set_state(RegistrationStates.waiting_university)
