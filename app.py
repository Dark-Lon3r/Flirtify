from loader import bot, CallbackQuery, Message, dp, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.keyboards import Ancketa_main
from locales.translate import translate, translate_key
from userdata.func_sql import user_languag, info_user_complaints, check_ban_user, add_user_waiting, info_anketa

from imports import aiosqlite, asyncio
from fuzzywuzzy import fuzz


async def find_matching_profiles(my_hobbies, profile_hobbies, threshold):
    similarity = fuzz.token_set_ratio(my_hobbies, profile_hobbies)
    return similarity >= threshold


async def get_random_profile(user_id, threshold):
    async with aiosqlite.connect("userdata.db") as db:
        query = """
            SELECT id, name, age, gender, description, hobbies, location, photo
            FROM anketa
            WHERE id NOT IN (
                SELECT profile_id FROM shown_profiles WHERE user_id = ?
            ) 
                AND id != ? 
                AND location = (
                    SELECT location_search FROM anketa WHERE id = ?
                )
                AND age <= (
                    SELECT age FROM anketa WHERE id = ?
                )
                AND gender IN (
                    SELECT search_gender FROM anketa WHERE id = ?
                )
            ORDER BY RANDOM()
            LIMIT 5
        """
        async with db.execute(query, (user_id, user_id, user_id, user_id, user_id)) as cursor:
            rows = await cursor.fetchall()
            if rows:
                profile_ids = [row[0] for row in rows]
                my_hobbies_query = "SELECT hobbies FROM anketa WHERE id = ?"
                async with db.execute(my_hobbies_query, (user_id,)) as my_hobbies_cursor:
                    my_hobbies_result = await my_hobbies_cursor.fetchone()
                    if my_hobbies_result:
                        my_hobbies = my_hobbies_result[0]
                        if my_hobbies:
                            for row in rows:
                                profile_hobbies = row[5]  # hobbies is the sixth column in the result
                                if profile_hobbies and await find_matching_profiles(my_hobbies, profile_hobbies, threshold):
                                    await db.execute("INSERT OR IGNORE INTO shown_profiles (user_id, profile_id) VALUES (?, ?)", (user_id, profile_ids[0]))
                                    await db.commit()
                    
                                    return row


@dp.callback_query_handler(lambda c: c.data == "start_ancket")
async def send_profile(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    await callback_query.message.delete()
    user_check_ban = await check_ban_user(callback_query.from_user.id, )

    if user_check_ban == callback_query.from_user.id:
        await bot.send_message(callback_query.from_user.id, '🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')

    else:
        user_info_complaints = await info_user_complaints(callback_query.from_user.id, )
        if user_info_complaints is not None:
            if int(user_info_complaints[0]) < 5:
                loop = asyncio.get_event_loop()
                task = loop.create_task(get_random_profile(callback_query.from_user.id, 30, ))
                await task

                profile = task.result()

                if profile:
                    id, name, age, gender, description, hobbies, location, photo = profile
                    file_path, text = await info_anketa(id, )
                    
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    markup.add(types.InlineKeyboardButton(text="👍", callback_data=f"like_{id}"),
                               types.InlineKeyboardButton(text="👎", callback_data=f"dislike_{id}"))
                    
                    await bot.send_photo(chat_id=callback_query.from_user.id, photo=open(f"{file_path}", "rb"), caption=text, reply_markup=markup)
                
                else:
                    user_languages = await user_languag(callback_query.from_user.id, )
                    ancketa_main = Ancketa_main(user_languages)
                    await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "no_users"), reply_markup = await ancketa_main.get_menu_keyboard_ancketa())

            else:
                user_languages = await user_languag(callback_query.from_user.id, )
                ancketa_main = Ancketa_main(user_languages)  
                await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "check_complaints_admins"), reply_markup = await ancketa_main.get_menu_keyboard_ancketa())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('like_', 'dislike_')))
async def process_callback_data(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text=f"{callback_query.data}")
    _, user_id = callback_query.data.split("_")
    user_id = int(user_id)
    
    async with aiosqlite.connect("userdata.db") as db:
        if callback_query.data.startswith("like"):
            await db.execute("UPDATE rating SET likes = likes + 1 WHERE id = ?", (user_id,))
            await db.commit()

            # Получаем информацию о пользователе, которому лайкнули анкету
            query = """SELECT id FROM anketa WHERE id = ?"""
            async with db.execute(query, (user_id,)) as cursor:
                result = await cursor.fetchone()
                if result:
                    # Отправляем пользователю, которому лайкнули анкету, сообщение с анкетой
                    id = result[0]                        
                    # Создаем кнопку "Отправить SMS" с ссылкой на аккаунт пользователя
                    user_name, user_name_send, id_first_sms = callback_query.from_user.username, callback_query.from_user.username, callback_query.from_user.id
                    id_send = callback_query.from_user.id
                    profile_choise = InlineKeyboardMarkup(row_width=2, inline_keyboard=True)
                    profile_choise.add(
                        InlineKeyboardButton("❤️", callback_data=f'likechoise/{user_name}/{id_first_sms}'),
                        InlineKeyboardButton("💔", callback_data=f'dislikechoise/{user_name}'),
                        InlineKeyboardButton("🚨", callback_data=f'complaints/{id_send}/{user_name_send}/{id}'),
                    )
                    loop = asyncio.get_event_loop()
                    task = loop.create_task(add_user_waiting(callback_query.from_user.id, 'like', id, ))
                    await task

            # Отправляем пользователю следующую анкету
            await send_profile(callback_query)

        elif callback_query.data.startswith("dislike"):
            await bot.answer_callback_query(callback_query_id=callback_query.id)
            await db.execute("UPDATE rating SET dislikes = dislikes + 1 WHERE id = ?", (user_id,))
            await db.commit()
            await send_profile(callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('likechoise/', 'dislikechoise/', 'complaints/', 'send_sms_first/')))
async def process_callback_data(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    await callback_query.message.delete()
    if callback_query.data.startswith('likechoise/'):
        user_id = callback_query.data.split("/")
        user_name = user_id[1]
        id_first_sms = user_id[2]
        await bot.answer_callback_query(callback_query.id, text=f"{callback_query.data}")

        user_profile_url = f"https://t.me/{user_name}"
        reply_markup = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
        reply_markup.add(
            InlineKeyboardButton("💌", url=user_profile_url),
            InlineKeyboardButton("📤", callback_data=f'send_sms_first/{id_first_sms}'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "like_choise_sms"), reply_markup = reply_markup)

    elif callback_query.data.startswith('dislikechoise/'):
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        user_languages = await user_languag(callback_query.from_user.id, )
        ancketa_main = Ancketa_main(user_languages)
        await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "menu_main"), reply_markup = await ancketa_main.get_menu_keyboard_ancketa())

    elif callback_query.data.startswith('complaints/'):
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        data_parts = callback_query.data.split('/')
        id_send = data_parts[1]
        user_name_send = data_parts[2]
        id = data_parts[3]
        
        user_languages = await user_languag(callback_query.from_user.id, )

        lang = user_languages
        translations = translate_key(lang)
        complaints_send = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        complaints_send.add(
            InlineKeyboardButton(translations['spam'][lang], callback_data=f'spam/{id_send}/{user_name_send}/{id}'),
            InlineKeyboardButton(translations['incorrect_behavior'][lang], callback_data=f'incorrect_behavior/{id_send}/{user_name_send}/{id}'),
            InlineKeyboardButton(translations['fake_profile'][lang], callback_data=f'fake_profile/{id_send}/{user_name_send}/{id}'),
            InlineKeyboardButton(translations['cyberbullying'][lang], callback_data=f'cyberbullying/{id_send}/{user_name_send}/{id}'),
            InlineKeyboardButton('❌', callback_data='cancel')
        )

        await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "complaints_info"), reply_markup = complaints_send)

    elif callback_query.data.startswith('send_sms_first/'):
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        id_first_sms = callback_query.data.split('/')[1]

        send_user_sms = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        send_user_sms.add(
            InlineKeyboardButton('💌', url=f'https://t.me/{callback_query.from_user.username}'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        await add_user_waiting(callback_query.from_user.id, 'sms_first', id_first_sms)
        user_languages = await user_languag(callback_query.from_user.id, )
        menu_ancketa = Ancketa_main(user_languages)
        await bot.send_message(callback_query.from_user.id, await translate(callback_query.from_user.id, "success"), reply_markup = await menu_ancketa.get_menu_keyboard_ancketa())