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
