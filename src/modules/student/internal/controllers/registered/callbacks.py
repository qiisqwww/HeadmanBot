@registration_callbacks_router.callback_query(AccessCallbackData.filter())
@logger.catch
async def accept_or_deny_callback(
    callback: CallbackQuery, callback_data: AccessCallbackData, bot: Bot, con: PoolConnectionProxy, redis_con: Redis
) -> None:
    if callback.message is None:
        return

    cache_student_service = CacheStudentService(redis_con)
    student_data = await cache_student_service.pop_student_cache(callback_data.student_id)

    if not callback_data.accepted:
        await callback.message.edit_text(REGISTRATION_DENIED_TEMPLATE, reply_markup=inline_void_button())
        await bot.send_message(student_data.telegram_id, YOU_WERE_DENIED_TEMPLATE)
        return

    registration_service = StudentService(con)
    await registration_service.register_student(student_data)

    # await bot.send_message(
    #     user_data["telegram_id"], YOU_WERE_ACCEPTED_TEMPLATE, reply_markup=default_buttons(user_data["role"])
    # )
    await bot.send_message(callback_data.student_id, YOU_WERE_ACCEPTED_TEMPLATE)
    await callback.message.edit_text(REGISTRATION_ACCEPTED_TEMPLATE, reply_markup=inline_void_button())
