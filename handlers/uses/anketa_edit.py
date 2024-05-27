from loader import bot, Message, CallbackQuery, dp, types

from keyboards.keyboards import Ancketa_main, Settings, Hobbies
from locales.translate import translate
from userdata.func_sql import get_user_info, edit_user_data, user_languag
from imports import FSMContext, State, StatesGroup, Text, ContentType
from imports import os, Nominatim, Location


class EditAncketaUser(StatesGroup):
	"""Редактирование акнты пользователя"""		
	EDIT_AGE = State()
	EDIT_NAME = State()
	PHOTO_EDIT = State()
	DESCRIPTION_EDIT = State()
	LOCATION_EDIT = State()
	LOCATION_EDIT_INPUT = State()
	HOBBIES_EDIT = State()
	
	SEARCH_GENDER_EDIT = State()
	LOCATION_SEARCH_EDIT = State()

	INSTAGRAM = State()
	TIKTOK_ADD = State()
	TWITTER = State()


@dp.message_handler(state=EditAncketaUser.PHOTO_EDIT, content_types=['photo'])
async def photo_edit(message: Message, state: FSMContext):
	if message.photo:
		user_languages = await user_languag(message.from_user.id, )
		user_info = await get_user_info(message.from_user.id)
		
		if user_info:
			file_path = user_info['photo']
			if os.path.isfile(file_path):
				os.remove(file_path)

		photo_id = message.photo[-1].file_id
		photo = await bot.get_file(photo_id)
	    
	    # Получаем расширение файла из file_path
		file_extension = os.path.splitext(photo.file_path)[-1]
	    
		photo_path = os.path.join("photo_users", f"{message.from_user.id}{file_extension}")
		await photo.download(destination_file=photo_path)
		await edit_user_data(message.from_user.id, 'photo', photo_path)
		await state.finish()

		main = Ancketa_main(user_languages)
		await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
		await message.delete()
		await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())

	elif not message.photo:
		await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
		await message.delete()
		await bot.send_message(message.from_user.id, await translate(callback_query.from_user.id, "edit_photo_users"))


@dp.message_handler(state=EditAncketaUser.EDIT_AGE)
async def edit_age_func(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		if not message.text.isdigit():
			settings = Settings(user_languages)
			await bot.send_message(message.from_user.id, await translate(message.from_user.id, "error_age"), reply_markup = await settings.get_menu_cancel())

		else:
			age = int(message.text)
			if 14 <= age <= 45:
				data['age'] = message.text
				
				await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
				await message.delete()
				await edit_user_data(message.from_user.id, 'age', data['age'])
				await state.finish()

				main = Ancketa_main(user_languages)
				await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())

			else:
				settings = Settings(user_languages)
				await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
				await message.delete()
				await bot.send_message(message.from_user.id, await translate(message.from_user.id, "error_age_low"), reply_markup = await settings.get_menu_cancel())


@dp.message_handler(state=EditAncketaUser.EDIT_NAME)
async def edit_name_func(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		data['name'] = message.text
		
		await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
		await message.delete()
		await edit_user_data(message.from_user.id, 'name', data['name'])
		await state.finish()

		main = Ancketa_main(user_languages)
		await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())


@dp.message_handler(state=EditAncketaUser.DESCRIPTION_EDIT)
async def destination_edit(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		data['description'] = message.text
		
		await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
		await message.delete()
		await edit_user_data(message.from_user.id, 'description', data['description'])
		await state.finish()

		main = Ancketa_main(user_languages)
		await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())


@dp.message_handler(state=EditAncketaUser.LOCATION_SEARCH_EDIT)
async def location_edit_search(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		data['location_search'] = message.text
		
		await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
		await message.delete()
		await edit_user_data(message.from_user.id, 'location_search', data['location_search'])
		await state.finish()

		main = Ancketa_main(user_languages)
		await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())


@dp.callback_query_handler(state=EditAncketaUser.SEARCH_GENDER_EDIT)
async def search_gender_edit(callback_query: CallbackQuery, state: FSMContext):
	user_languages = await user_languag(callback_query.from_user.id, )
	async with state.proxy() as data:
		data['search_gender'] = callback_query.data
		
		await callback_query.message.delete()
		await edit_user_data(callback_query.from_user.id, 'search_gender', data['search_gender'])
		await state.finish()

		main = Ancketa_main(user_languages)
		await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())


@dp.message_handler(content_types=[ContentType.LOCATION], state=EditAncketaUser.LOCATION_EDIT)
async def location_edit(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	location = message.location
	async with state.proxy() as data:
		if 'location' in data and data['location'] is not None:
			data['location'].latitude = location.latitude
			data['location'].longitude = location.longitude
		else:
			data['location'] = Location(latitude=location.latitude, longitude=location.longitude)
        
		geolocator = Nominatim(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
		location_info = geolocator.reverse(f"{location.latitude}, {location.longitude}", exactly_one=True, timeout=10)
		location = location_info.raw.get('address', {}).get('city', 'Неизвестно')

		await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
		await message.delete()
		await edit_user_data(message.from_user.id, 'location', location)
		await state.finish()

		main = Ancketa_main(user_languages)
		await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())


@dp.message_handler(state=EditAncketaUser.LOCATION_EDIT_INPUT)
async def process_location(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		location_text = message.text

        # Проверяем наличие буквы "ы" в строке и заменяем её на "и"
		if 'ы' in location_text:
			location_text = location_text.replace('ы', 'и')

	await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
	await message.delete()
	await edit_user_data(message.from_user.id, 'location', location_text)
	await state.finish()

	main = Ancketa_main(user_languages)
	await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())


# Обработчик выбора категории хобби
@dp.callback_query_handler(lambda query: query.data.startswith('category_'), state=EditAncketaUser.HOBBIES_EDIT)
async def edit_hobby_category(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)

    category = callback_query.data.split('_')[1]
    hobbies = Hobbies()
    # В зависимости от выбранной категории, отправляем соответствующее меню с хобби
    if category == 'it':
        await callback_query.message.edit_text("<i>👾 Ого, вже знаходишся в категорії IT/Технології! Я впевнений, ти знайдеш тут щось цікаве, так само як і мене 😉💻</i>", reply_markup= await hobbies.get_menu_hobbies_it())
    elif category == 'sport':
        await callback_query.message.edit_text("<i>🔥 Вибери своє спортивне хобі! Чи знаєш, що спорт піднімає не тільки настрій, але й температуру? 😏 Обери спорт, який тобі до вподоби, і ми знайдемо тобі співрозмовника, з яким ти зможеш спалити зайві калорії! 💪🔥</i>", reply_markup= await hobbies.get_menu_hobbies_sport())
    elif category == 'cooking':
        await callback_query.message.edit_text("<i>🍳 Ой, оскільки ми розмовляємо про кулінарію, дозволь мені розпалити твої кулінарні фантазії! 😏🔥 Обери кулінарний шлях, а я покажу тобі, що подібність в смаках може призвести до неймовірного зв'язку! 💕</i>", reply_markup= await hobbies.get_menu_hobbies_cooking())
    elif category == 'creativity':
        await callback_query.message.edit_text("<i>🎨 Ох, ми дійшли до категорії Творчість та Мистецтво! Тут наше спілкування може стати справжнім мистецтвом, а твоя креативність зацікавить мене ще більше! 😏💫</i>", reply_markup= await hobbies.get_menu_hobbies_creativity())
    elif category == 'back':
        await callback_query.message.edit_text("<i>Я чув, що хобі - це те, що ти робиш із задоволенням, навіть якщо ніхто не дивиться. \nТо що, яке твоє хобі? 😉</i>", reply_markup = await hobbies.get_menu_hobbies_choose())

    # Сохраняем выбранную категорию в состоянии
    async with state.proxy() as data:
        data['category'] = category


# Обработчик выбора конкретного хобби
@dp.callback_query_handler(lambda query: query.data.startswith('hobby_'), state=EditAncketaUser.HOBBIES_EDIT)
async def edit_hobby_selection(callback_query: CallbackQuery, state: FSMContext):
	await bot.answer_callback_query(callback_query_id=callback_query.id)
	hobby = callback_query.data.split('_')[1]
	user_languages = await user_languag(callback_query.from_user.id, )    

	await edit_user_data(callback_query.from_user.id, 'hobbies', hobby)

	main = Ancketa_main(user_languages)
	await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'success'), reply_markup = await main.get_menu_keyboard_ancketa())
	await state.finish()


@dp.message_handler(state=EditAncketaUser.INSTAGRAM)
async def instagram_add(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		if message.text.startswith('https://instagram.com/'):
			data['instagram'] = message.text

			await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
			await message.delete()
			await edit_user_data(message.from_user.id, 'instagram', data['instagram'])
			await state.finish()

			main = Ancketa_main(user_languages)
			await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())

		else:
			settings = Settings(user_languages)
			await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
			await message.delete()
			await bot.send_message(message.from_user.id, await translate(message.from_user.id, "instagram_error_link"), reply_markup = await settings.get_menu_cancel())


@dp.message_handler(state=EditAncketaUser.TIKTOK_ADD)
async def tiktok_add(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		if message.text.startswith('https://www.tiktok.com/@'):
			data['tiktok'] = message.text

			await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
			await message.delete()
			await edit_user_data(message.from_user.id, 'tiktok', data['tiktok'])
			await state.finish()

			main = Ancketa_main(user_languages)
			await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())

		else:
			settings = Settings(user_languages)
			await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
			await message.delete()
			await bot.send_message(message.from_user.id, await translate(message.from_user.id, "tiktok_error_link"), reply_markup = await settings.get_menu_cancel())


@dp.message_handler(state=EditAncketaUser.TWITTER)
async def twitter_add(message: Message, state: FSMContext):
	user_languages = await user_languag(message.from_user.id, )
	async with state.proxy() as data:
		if message.text.startswith('https://twitter.com/'):
			data['twitter'] = message.text

			await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
			await message.delete()
			await edit_user_data(message.from_user.id, 'twitter', data['twitter'])
			await state.finish()

			main = Ancketa_main(user_languages)
			await bot.send_message(message.from_user.id, await translate(message.from_user.id, "success"), reply_markup = await main.get_menu_keyboard_ancketa())

		else:
			settings = Settings(user_languages)
			await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
			await message.delete()
			await bot.send_message(message.from_user.id, await translate(message.from_user.id, "twitter_error_link"), reply_markup = await settings.get_menu_cancel())
