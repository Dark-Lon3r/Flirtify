from loader import bot, CallbackQuery, Message, dp, types

from keyboards.keyboards import Admin, InlineKeyboardButton, InlineKeyboardMarkup
from userdata.func_sql import get_user_info
from handlers.ban.ban import ban_user_func, no_ban_user_func
from imports import aiosqlite

menu_moderation = Admin()

async def list_complaints_db():
    async with aiosqlite.connect("userdata.db") as db:
        query = "SELECT id, name, username, send_complaints_id, send_complaints_username, send_complaints_catigories FROM complaints WHERE value_complaints > 4"
        async with db.execute(query) as cursor:
            results = await cursor.fetchall()
            return results


async def moderation_func(callback_query: CallbackQuery):
	await callback_query.message.edit_text('🌟 Вітаю в Меню Модерації! Тут вирішуються судьби анкет, а ти - головний суддя! 👩‍⚖️🤵', reply_markup = await menu_moderation.get_moderation_menu())


@dp.callback_query_handler(lambda c: c.data == 'list_complaints')
async def list_complaints_check(callback_query: CallbackQuery):
    list_result = await list_complaints_db()
    user_index = 0  # Переменная для отслеживания текущего индекса жалобы

    if list_result:
        await show_complaint(callback_query.from_user.id, list_result, user_index)
    else:
        await callback_query.message.edit_text("Нет пользователей с жалобами", reply_markup = await menu_moderation.get_moderation_menu())


async def show_complaint(chat_id, complaints_list, index):
    result = complaints_list[index]
    complaint_id = result[0]
    name = result[1]
    username = result[2]
    send_complaints_id = result[3]
    send_complaints_username = result[4]
    send_complaints_categories = result[5]

    message = "<b>Список пользователей с жалобами:</b>\n\n"
    user_info = f"ID: {complaint_id}\n"
    user_info += f"Имя: {name}\n"
    user_info += f"Имя пользователя: @{username}\n\n"
    user_info += f"ID отправителя жалобы: {send_complaints_id}\n"
    user_info += f"Имя пользователя отправителя жалобы: @{send_complaints_username}\n"
    user_info += f"Категории жалобы: {send_complaints_categories}\n\n"
    message += user_info

    moderation_ban = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    moderation_ban.add(
        InlineKeyboardButton('💔Забанить пользователя', callback_data=f'ban_{index}_{complaint_id}_{username}'),
        InlineKeyboardButton('💞Простить', callback_data=f'noban_{index}_{complaint_id}_{username}'),
        InlineKeyboardButton('Следующая жалоба', callback_data=f'next_{index+1}'),
        InlineKeyboardButton('❌', callback_data='cancel')
    )

    await bot.send_message(chat_id, message, reply_markup=moderation_ban)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('ban_', 'noban_', 'next_')))
async def ban_user(callback_query: CallbackQuery):
    data_parts = callback_query.data.split("_")
    action = data_parts[0]
    user_index = int(data_parts[1])

    if action == "ban":
        complaint_id = int(data_parts[2])  # Получаем идентификатор жалобы из коллбэк-данных
        username = data_parts[3]  # Получаем имя пользователя

        await ban_user_func(complaint_id, )
        ban_sms_key = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        ban_sms_key.add(
            InlineKeyboardButton('💔', callback_data='key_ban')
        )
        await bot.send_message(complaint_id, "На жаль, ваша анкета перевищила квоту жалоб і отримала спеціальний бан-трофей. Ваш успіх вражає! 🚫🏆", reply_markup = ban_sms_key)
        await callback_query.message.edit_text(f"Вы забанили пользователя с индексом {user_index}, ID жалобы {complaint_id}, {username}")

    elif action == "noban":
        complaint_id = int(data_parts[2])  # Получаем идентификатор жалобы из коллбэк-данных
        username = data_parts[3]  # Получаем имя пользователя

        await no_ban_user_func(complaint_id, )
        await bot.send_message(complaint_id, "У нас є чудова новина: жалоби були відправлені на курорт, а ви отримали статус 'Прощених'! Ви найкраще лікування для нашого проекту! 🌴❌")
        await callback_query.message.edit_text(f"Вы отклонили бан пользователя с индексом {user_index}, ID жалобы {complaint_id}, {username}")

    elif action == "next":
        list_result = await list_complaints_db()
        next_index = int(data_parts[1])

        if next_index < len(list_result):
            await show_complaint(callback_query.from_user.id, list_result, next_index)
        else:
            await callback_query.message.edit_text("Достигнут конец списка жалоб", reply_markup = await menu_moderation.get_moderation_menu())
