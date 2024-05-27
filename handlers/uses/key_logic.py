from loader import bot, CallbackQuery, Message, dp, types

from keyboards.keyboards import Ancketa_main, Settings, Menu, Pay, Floor, Hobbies, InlineKeyboardMarkup, InlineKeyboardButton
from userdata.func_sql import get_user_info, user_languag, edit_user_data, check_admin_moderation, create_user_data, check_ban_user, check_waiting, info_anketa, info_waiting

from handlers.admin.admin import admin_func
from handlers.moderation.moderation_logic import moderation_func
from handlers.uses.anketa_edit import *

from locales.translate import translate

from imports import Nominatim, FSMContext, aiosqlite, lru_cache, cache, asyncio



@dp.callback_query_handler(lambda c: c.data == 'my_ancketa')
async def my_ancketa_func(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    await callback_query.message.delete()

    user_check_ban = await check_ban_user(callback_query.from_user.id, )

    if user_check_ban == callback_query.from_user.id:
        await bot.send_message(callback_query.from_user.id, '🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')

    else:
        file_path, text = await info_anketa(callback_query.from_user.id,  )
        user_languages = await user_languag(callback_query.from_user.id, )
        
        settings = Settings(user_languages)
        await bot.send_photo(chat_id=callback_query.from_user.id, photo=open(f"{file_path}", "rb"), caption=text, parse_mode="HTML", reply_markup = await settings.get_menu_back())
        await bot.answer_callback_query(callback_query_id=callback_query.id)


@dp.callback_query_handler(lambda c:c.data == 'cancel', state = '*')
async def btnCancel(callback_query: CallbackQuery, state: FSMContext):
    user_check_ban = await check_ban_user(callback_query.from_user.id, )
    await state.finish()

    if user_check_ban == callback_query.from_user.id:
        await callback_query.message.edit_text('🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')

    else:
        id_admin, id_moderation = await check_admin_moderation(callback_query.from_user.id)
        user_languages = await user_languag(callback_query.from_user.id, )
        main = Ancketa_main(user_languages)

        if id_admin == callback_query.from_user.id or id_moderation == callback_query.from_user.id:
            await callback_query.message.edit_text(await translate(callback_query.from_user.id, "menu_main"), reply_markup = await main.get_menu_judging())
        
        else:
            await callback_query.message.edit_text(await translate(callback_query.from_user.id, "menu_main"), reply_markup = await main.get_menu_keyboard_ancketa())
            await bot.answer_callback_query(callback_query_id=callback_query.id)


@dp.message_handler(commands=['menu'])
async def send_menu(message: Message, state: FSMContext):
    
    if await get_user_info(message.from_user.id) is not None:
        user_check_ban = await check_ban_user(message.from_user.id, )
        if user_check_ban == message.from_user.id:
            await bot.send_message(message.from_user.id, '🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')
            await message.delete()

        else:
            if not os.path.isfile("userdata.db"):
                await create_user_data(message.from_user.id)  

            else:
                id_admin, id_moderation = await check_admin_moderation(message.from_user.id)
                user_languages = await user_languag(message.from_user.id, )
                main = Ancketa_main(user_languages)
                
                if id_admin == message.from_user.id or id_moderation == message.from_user.id:
                    await bot.send_message(message.from_user.id, await translate(message.from_user.id, "menu_main"), reply_markup = await main.get_menu_judging())

                else:
                    await bot.send_message(message.from_user.id, await translate(message.from_user.id, "menu_main"), reply_markup = await main.get_menu_keyboard_ancketa())

    else:
        await create_user_data(message.from_user.id)
        # пользователь не найден
        menu_main = Menu()
        await bot.send_message(message.from_user.id, "<i>💬Привіт! Я Flirtify – твій персональний купідон. Хочеш спробувати свій успіх у знайомствах? Давай почнемо!🏹</i>", reply_markup = await menu_main.get_menu_keyboard_start())


@dp.callback_query_handler(lambda c: c.data == 'back')
async def back(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)

    user_check_ban = await check_ban_user(callback_query.from_user.id, )
    if user_check_ban == callback_query.from_user.id:
        await callback_query.message.edit_text('🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')

    else:
        user_languages = await user_languag(callback_query.from_user.id, )
        main = Ancketa_main(user_languages)
        id_admin, id_moderation = await check_admin_moderation(callback_query.from_user.id)
        
        if callback_query.message.photo:
            await callback_query.message.delete()            
            if id_admin == callback_query.from_user.id or id_moderation == callback_query.from_user.id:
                await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "menu_main"), reply_markup=await main.get_menu_judging())

            else:
                await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "menu_main"), reply_markup=await main.get_menu_keyboard_ancketa())

        else:
            if id_admin == callback_query.from_user.id or id_moderation == callback_query.from_user.id:
                await callback_query.message.edit_text(await translate(callback_query.from_user.id, "menu_main"), reply_markup=await main.get_menu_judging())

            else:
                await callback_query.message.edit_text(await translate(callback_query.from_user.id, "menu_main"), reply_markup=await main.get_menu_keyboard_ancketa())




@dp.callback_query_handler(lambda c: c.data == 'settings')
async def settings_key(callback_query: CallbackQuery):
    user_check_ban = await check_ban_user(callback_query.from_user.id, )
    if user_check_ban == callback_query.from_user.id:
        await callback_query.message.edit_text('🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')

    else:
        user_languages = await user_languag(callback_query.from_user.id, )
        settings = Settings(user_languages)

        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "settings_info"), reply_markup = await settings.keyboard_choice_ancketa())
        await bot.answer_callback_query(callback_query_id=callback_query.id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('search', 'settings_ancketa', 'social')))
async def settings_key_choice(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    user_languages = await user_languag(callback_query.from_user.id, )
    settings = Settings(user_languages)

    if callback_query.data.startswith('search'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'search'), reply_markup = await settings.settings_search())

    elif callback_query.data.startswith('settings_ancketa'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'settings_edit_anketa'), reply_markup = await settings.get_menu_settings_anketa())

    elif callback_query.data.startswith('social'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'social'), reply_markup = await settings.settings_social()) 


#settings_ancketa
@cache
@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('edit_age', 'edit_name', 'edit_photo', 'edit_description', 'edit_location', 'edit_hobbies', 'edit_languages', 'key_ban')))
async def settings_key_anketa(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    user_languages = await user_languag(callback_query.from_user.id, )
    settings = Settings(user_languages)

    if callback_query.data.startswith('edit_age'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "edit_age"), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.EDIT_AGE.set()

    elif callback_query.data.startswith('edit_name'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "edit_name"), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.EDIT_NAME.set()

    elif callback_query.data.startswith('edit_photo'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "edit_photo_users"), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.PHOTO_EDIT.set()

    elif callback_query.data.startswith('edit_description'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "destination_edit_users"), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.DESCRIPTION_EDIT.set()

    elif callback_query.data.startswith('edit_location'):
        key_location = Ancketa_main(user_languages)
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "location_edit_users"), reply_markup = await key_location.get_menu_choice_location())
    
    elif callback_query.data.startswith('edit_hobbies'):
        menu_hobbies = Hobbies()
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "edit_hobbies_users"), reply_markup = await menu_hobbies.get_menu_hobbies_choose())
        await EditAncketaUser.HOBBIES_EDIT.set()

    elif callback_query.data.startswith('edit_languages'):
        key_languages = Settings("uk")
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "edit_languages_users"), reply_markup = await key_languages.get_menu_keyboard_languages())


#settings_search
@cache
@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('edit_search_gender', 'edit_search_location')))
async def settings_key_search(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    user_languages = await user_languag(callback_query.from_user.id, )
    settings = Settings(user_languages)

    if callback_query.data.startswith('edit_search_location'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "location_edit_search_users"), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.LOCATION_SEARCH_EDIT.set()

    elif callback_query.data.startswith('edit_search_gender'):
        menu = Floor()
        await callback_query.message.edit_text("🔎🔎💑", reply_markup = await menu.get_menu_keyboard())
        await EditAncketaUser.SEARCH_GENDER_EDIT.set()

#social_key
@cache
@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('add_instagram', 'add_tiktok', 'add_twitter')))
async def settings_key_social(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    user_languages = await user_languag(callback_query.from_user.id, )
    settings = Settings(user_languages)

    if callback_query.data.startswith('add_instagram'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'add_instagram'), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.INSTAGRAM.set()

    elif callback_query.data.startswith('add_tiktok'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'add_tiktok'), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.TIKTOK_ADD.set()

    elif callback_query.data.startswith('add_twitter'):
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'add_twitter'), reply_markup = await settings.get_menu_cancel())
        await EditAncketaUser.TWITTER.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('btn1', 'btn2')))
async def choice_location(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    if callback_query.data.startswith("btn1"):
        user_languages = await user_languag(callback_query.from_user.id, )

        key_location = Ancketa_main(user_languages)
        
        await callback_query.message.edit_text("<i>🌍 Активуй свій GPS-приймач і тисни кнопку нижче, щоб ми знайшли тебе! 📍🛰️</i>", reply_markup = await key_location.get_menu_keyboard_ancketa_location())
        await EditAncketaUser.LOCATION_EDIT.set()

    elif callback_query.data.startswith("btn2"):
        await callback_query.message.edit_text("<i>🏙️ Ти наш супергеограф! Введи своє місто самостійно і дай нам знати, де тебе можна зустріти на романтичний поцілунок! 😘🌆</i>")
        await EditAncketaUser.LOCATION_EDIT_INPUT.set()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('uk_lang', 'ru_lang')))
async def process_languages(callback_query: types.CallbackQuery):
    user_languages = await user_languag(callback_query.from_user.id, )
    if callback_query.data.startswith("uk_lang"):
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        await edit_user_data(callback_query.from_user.id, 'languages', 'uk')
        
        main = Ancketa_main(user_languages)
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "menu_main"), reply_markup = await main.get_menu_keyboard_ancketa())
        

    elif callback_query.data.startswith("ru_lang"):
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        await edit_user_data(callback_query.from_user.id, 'languages', 'ru')
        
        main = Ancketa_main(user_languages)
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "menu_main"), reply_markup = await main.get_menu_keyboard_ancketa())


@dp.callback_query_handler(lambda c: c.data == 'status_notification')
async def status_notification_func(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    user_check_ban = await check_ban_user(callback_query.from_user.id, )

    if user_check_ban == callback_query.from_user.id:
        await callback_query.message.edit_text('🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')

    else:
        total_count = await check_waiting(callback_query.from_user.id, ) 
        _, categories = await info_waiting(callback_query.from_user.id, )
        user_languages = await user_languag(callback_query.from_user.id, )
        main = Ancketa_main(user_languages)

        if int(total_count) > 0:
            if categories == 'like':
                menu_notification_anketa = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
                menu_notification_anketa.add(
                    InlineKeyboardButton('💓👀', callback_data='notification_anketa')
                )
                await callback_query.message.edit_text(await translate(callback_query.from_user.id, "notification_like") + f"\n🛎 :{total_count}", reply_markup = menu_notification_anketa)

            elif categories == 'sms_first':
                menu_notification_like = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
                menu_notification_like.add(
                    InlineKeyboardButton('💌', callback_data='notification_sms')
                )
                await callback_query.message.edit_text(await translate(callback_query.from_user.id, "notification_sms"), reply_markup = menu_notification_like)

        else:
            await callback_query.message.edit_text(await translate(callback_query.from_user.id, "no_notification"), reply_markup = await main.get_menu_keyboard_ancketa())               


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('notification_anketa', 'notification_sms')))
async def notification_func(callback_query: CallbackQuery):
    id_send_waiting, _ = await info_waiting(callback_query.from_user.id, )
    file_path, text = await info_anketa(id_send_waiting, )
    id_my = callback_query.from_user.id

    if callback_query.data.startswith('notification_anketa'):
        await callback_query.message.delete()
        username_send = (await bot.get_chat(id_send_waiting)).username
        
        profile_choise = InlineKeyboardMarkup(row_width=2, inline_keyboard=True)
        profile_choise.add(
            InlineKeyboardButton("❤️", callback_data=f'likechoise/{username_send}/{id_send_waiting}'),
            InlineKeyboardButton("💔", callback_data=f'dislikechoise/{username_send}'),
            InlineKeyboardButton("🚨", callback_data=f'complaints/{id_my}/{username_send}/{id_send_waiting}'),
        )

        async with aiosqlite.connect("userdata.db") as db:
            await db.execute("DELETE FROM waiting WHERE id_waiting = ? AND (categories = ? OR id_send = ?) LIMIT 1", (id_my, 'like', id_send_waiting))
            await db.commit()

        await bot.send_photo(id_my, photo=open(f'{file_path}', 'rb'), caption=text, reply_markup = profile_choise)

    elif callback_query.data.startswith('notification_sms'):
        username_sms_callback = (await bot.get_chat(id_send_waiting)).username

        send_user_sms = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        send_user_sms.add(
            InlineKeyboardButton('💌', url=f'https://t.me/{username_sms_callback}'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        async with aiosqlite.connect("userdata.db") as db:
            await db.execute("DELETE FROM waiting WHERE id_waiting = ? AND (categories = ? OR id_send = ?) LIMIT 1", (id_my, 'sms_first', id_send_waiting))
            await db.commit()

        await callback_query.message.edit_text(await translate(id_send_waiting, "id_user_send_first"), reply_markup = send_user_sms)


@lru_cache
@dp.callback_query_handler(lambda c: c.data == 'donate')
async def edit_languages(callback_query: CallbackQuery):
    donate = Pay()
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    await callback_query.message.edit_text("💰💰💰💰💰💰💰💰💰💰💰", reply_markup = await donate.get_menu_donate())


@dp.callback_query_handler(lambda c: c.data == 'judging')
async def judging_menu(callback_query: CallbackQuery):
    id_admin, id_moderation = await check_admin_moderation(callback_query.from_user.id)
    if id_admin is not None:
        await admin_func(callback_query)
    elif id_moderation is not None:
        await moderation_func(callback_query)
