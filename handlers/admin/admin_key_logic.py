from loader import bot, CallbackQuery, Message, dp, types

from handlers.admin.admin import admin_key
from keyboards.keyboards import Admin, Ancketa_main
from userdata.func_sql import get_user_info

from imports import aiosqlite, State, StatesGroup, FSMContext


class AdminState(StatesGroup):
	"""Состояния Админки"""
	SMS_SEND_ALL = State()
	SMS_SEND_USER = State()
	ADD_MODERATION = State()
	DELETE_BAN_USER = State()


@dp.callback_query_handler(lambda c:c.data == 'cancel_admin', state = '*')
async def btnCancel(callback_query: CallbackQuery, state: FSMContext):
    if state is None:
        return

    await state.finish()

    await callback_query.message.edit_text(f"<b>❌ОТМЕНА И ОЧИСТКА СОСТОЯНИЙ❌</b>", reply_markup = await admin_key.get_admin_menu())
    await bot.answer_callback_query(callback_query_id=callback_query.id)


@dp.callback_query_handler(lambda c:c.data == 'exit_admin_menu')
async def exit_admin_func(callback_query: CallbackQuery):
	user_languages = await get_user_info(callback_query.from_user.id, )
	exit_admin = Ancketa_main(user_languages['languages'])
	
	await callback_query.message.edit_text("<b>EXIT ADMIN</b>", reply_markup = await exit_admin.get_menu_judging())


@dp.callback_query_handler(lambda c: c.data == 'clean_shown')
async def clean_shown_profiles(callback_query: CallbackQuery):
	async with aiosqlite.connect("userdata.db") as db:
		await db.execute("DELETE FROM shown_profiles")
		await db.commit()

		await callback_query.message.edit_text("<b>Успешно очищено</b>", reply_markup = await admin_key.get_admin_menu())


@dp.callback_query_handler(lambda c: c.data == 'send_users_sms')
async def clean_shown_profiles(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Что отправить?", reply_markup = await admin_key.get_admin_menu_cancel())
    await AdminState.SMS_SEND_ALL.set()


@dp.message_handler(state=AdminState.SMS_SEND_ALL)
async def send_set_sms(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['sms_all'] = message.text

	async with aiosqlite.connect("userdata.db") as db:
		query = "SELECT id FROM anketa"
		cursor = await db.execute(query)
		rows = await cursor.fetchall()

		for i in rows:
			await bot.send_message(i[0], f"{data['sms_all']}")

		await message.delete()
		await bot.send_message(message.chat.id, "Успешно отправлено", reply_markup = await admin_key.get_admin_menu())
		await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'add_moderation')
async def clean_shown_profiles(callback_query: CallbackQuery):
	await callback_query.message.delete()
	await bot.send_message(callback_query.from_user.id, "<i>Введи id пользователя которого требуется добавить в модеров</i>", reply_markup = await admin_key.get_admin_menu_cancel())
	await AdminState.ADD_MODERATION.set()


@dp.message_handler(state=AdminState.ADD_MODERATION)
async def send_set_sms(message: Message, state: FSMContext):
	async with state.proxy() as data:
		data['id_moderation'] = message.text

	async with aiosqlite.connect("userdata.db") as db:
	        await db.execute("""INSERT INTO admin_moderation (
	        	id_moderation) VALUES(?)""", 
	        	
	        	(int(data['id_moderation']), )
	        )

	        await db.commit()

	await state.finish()
	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
	await message.answer('<i>Успешно добавлен</i>', reply_markup = await admin_key.get_admin_menu())


@dp.callback_query_handler(lambda c: c.data == 'delete_ban_user')
async def delete_ban_user_func(callback_query: CallbackQuery):
	await callback_query.message.edit_text('Введи id пользователя которому нужно удалить бан', reply_markup = await admin_key.get_admin_menu_cancel())
	await AdminState.DELETE_BAN_USER.set()


@dp.message_handler(state=AdminState.DELETE_BAN_USER)
async def delete_ban(message: Message, state: FSMContext):
	async with state.proxy() as data:
		data['user'] = message.text

	async with aiosqlite.connect("userdata.db") as db:
		await db.execute("DELETE FROM ban WHERE id = ? ", (data['user'], ))
		await db.commit()

	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
	await message.answer('<i>Успешно снят бан с пользователя</i>', reply_markup=await admin_key.get_admin_menu())