from loader import bot, CallbackQuery, Message, dp, types

from keyboards.keyboards import Pay
from locales.translate import translate

from imports import lru_cache


@lru_cache
@dp.callback_query_handler(lambda c: c.data == 'monobank')
async def monobank_func(callback_query: CallbackQuery):
	donate = Pay()

	await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
	await bot.answer_callback_query(callback_query_id=callback_query.id)

	await bot.send_photo(callback_query.from_user.id, photo=open("photo_bot/monobank_qr_code.jpg", "rb") , caption = await translate(callback_query.from_user.id, "monobank"), reply_markup = await donate.get_menu_monobank())

@lru_cache
@dp.callback_query_handler(lambda c: c.data == 'gmail_send')
async def gmail_func(callback_query: CallbackQuery):
	donate = Pay()
	await callback_query.message.edit_text(await translate(callback_query.from_user.id, "gmail_send"), reply_markup = await donate.get_menu_donate())
