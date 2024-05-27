from loader import bot, CallbackQuery, Message, dp, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.keyboards import Ancketa_main
from locales.translate import translate
from userdata.func_sql import user_languag, edit_user_data_complaints


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('spam/', 'incorrect_behavior/', 'fake_profile/', 'cyberbullying/')))
async def process_languages(callback_query: types.CallbackQuery):
    user_languages = await user_languag(callback_query.from_user.id, )
    menu = Ancketa_main(user_languages)
    if callback_query.data.startswith('spam/'):
        data_parts = callback_query.data.split('/')
        id_send = data_parts[1]
        user_name_send = data_parts[2]
        id = data_parts[3]

        await edit_user_data_complaints(id_send, user_name_send, 'Спам' , int(1), id)
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'menu_main'), reply_markup = await menu.get_menu_keyboard_ancketa())

    elif callback_query.data.startswith('incorrect_behavior/'):
        data_parts = callback_query.data.split('/')
        id_send = data_parts[1]
        user_name_send = data_parts[2]
        id = data_parts[3]

        await edit_user_data_complaints(id_send, user_name_send, 'Некоректное поведение' , int(1), id)
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'menu_main'), reply_markup = await menu.get_menu_keyboard_ancketa())

    elif callback_query.data.startswith('fake_profile/'):
        data_parts = callback_query.data.split('/')
        id_send = data_parts[1]
        user_name_send = data_parts[2]
        id = data_parts[3]

        await edit_user_data_complaints(id_send, user_name_send, 'Фейк профиль' , int(1), id)
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'menu_main'), reply_markup = await menu.get_menu_keyboard_ancketa())

    elif callback_query.data.startswith('cyberbullying/'):
        data_parts = callback_query.data.split('/')
        id_send = data_parts[1]
        user_name_send = data_parts[2]
        id = data_parts[3]

        await edit_user_data_complaints(id_send, user_name_send, 'Кибербулинг' , int(1), id)
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, 'menu_main'), reply_markup = await menu.get_menu_keyboard_ancketa())
