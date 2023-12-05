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
