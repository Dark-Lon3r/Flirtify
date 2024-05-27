from loader import bot, dp, types, CallbackQuery, Message
from imports import FSMContext

from locales.translate import translate, translate_start
from userdata.func_sql import get_user_info, user_languag, check_admin_moderation, create_user_data, check_ban_user
from keyboards.keyboards import Menu, Ancketa_main
from handlers.uses.ancket_add import ancketa_create_user
from imports import os


@dp.message_handler(commands=['start'])
async def start(message: Message, state: FSMContext):
    if not os.path.isfile("userdata.db"):
        await create_user_data(message.from_user.id)    
    
    else:
        if await get_user_info(message.from_user.id) is not None:
            user_check_ban = await check_ban_user(message.from_user.id, )
            if user_check_ban == message.from_user.id:
                await bot.send_message(message.from_user.id, '🔒 Навіки заборонений! Відтепер ваша пригода у нашому проекті буде тривати тільки у легендах та спогадах! 🚫😢')

            else:
                # пользователь найден и не забанен
                id_admin, id_moderation = await check_admin_moderation(message.from_user.id)
                
                user_languages = await user_languag(message.from_user.id, )
                ancketa_main = Ancketa_main(user_languages)
                
                if id_admin == message.from_user.id or id_moderation == message.from_user.id:
                    await bot.send_message(message.from_user.id, await translate(message.from_user.id, "back_user"), reply_markup = await ancketa_main.get_menu_judging())
                    
                else:
                    await bot.send_message(message.from_user.id, await translate(message.from_user.id, "back_user"), reply_markup = await ancketa_main.get_menu_keyboard_ancketa())

        else:
            await create_user_data(message.from_user.id)
            menu_main = Menu()
            await bot.send_message(message.from_user.id, "<i>💬Привіт! Я Flirtify – твій персональний купідон. Хочеш спробувати свій успіх у знайомствах? Давай почнемо!🏹</i>", reply_markup = await menu_main.get_menu_keyboard_start())

dp.register_callback_query_handler(ancketa_create_user, lambda c: c.data == 'create_ancket')