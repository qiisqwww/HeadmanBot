from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from src.kernel import Router
from src.kernel.resources.buttons import inline_void_button
from src.modules.student.internal.controllers.unregistred.registration_context import (
    RegistrationContext,
)
from src.modules.student.internal.controllers.unregistred.registration_states import (
    RegistrationStates,
)
from src.modules.student.internal.gateways import UniversityGatewate
from src.modules.student.internal.resources.inline_buttons import (
    university_list_buttons,
)
from src.modules.student.internal.resources.templates import (
    ASK_GROUP_TEMPLATE,
    ASK_UNIVERSITY_TEMPLATE,
    CHOOSE_STUDENT_ROLE_TEMPLATE,
    succesfull_role_choose_template,
    succesfull_university_choose_template,
)
from src.modules.student.internal.services import CacheStudentService, StudentService

from .callback_data import RoleCallbackData, UniversityCallbackData

__all__ = [
    "registration_callbacks_router",
]


registration_callbacks_router = Router(
    must_be_registered=False,
    services={
        "university_gateway": UniversityGatewate,
        "cache_student_service": CacheStudentService,
        "student_service": StudentService,
    },
)


@registration_callbacks_router.callback_query(RoleCallbackData.filter())
@logger.catch
async def get_role_from_user(
    callback: CallbackQuery, callback_data: RoleCallbackData, state: FSMContext, university_gateway: UniversityGatewate
) -> None:
    registration_ctx = RegistrationContext(state)

    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await registration_ctx.set_role(callback_data.role)

    await callback.message.edit_text(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=inline_void_button())
    await callback.message.answer(succesfull_role_choose_template(await registration_ctx.role))

    universities = await university_gateway.get_all_universities()

    await callback.message.answer(text=ASK_UNIVERSITY_TEMPLATE, reply_markup=university_list_buttons(universities))
    await registration_ctx.set_state(RegistrationStates.waiting_university)


@registration_callbacks_router.callback_query(UniversityCallbackData.filter())
@logger.catch
async def get_university_from_user(
    callback: CallbackQuery,
    callback_data: UniversityCallbackData,
    state: FSMContext,
    university_gateway: UniversityGatewate,
) -> None:
    registration_ctx = RegistrationContext(state)

    if callback.message is None:
        return

    choosen_uni = await university_gateway.get_university_by_alias(callback_data.university_alias)

    await registration_ctx.set_university_alias(callback_data.university_alias)

    await callback.message.edit_text(ASK_UNIVERSITY_TEMPLATE, reply_markup=inline_void_button())
    await callback.message.answer(succesfull_university_choose_template(choosen_uni.name))
    await callback.message.answer(ASK_GROUP_TEMPLATE)

    await registration_ctx.set_state(RegistrationStates.waiting_group)
