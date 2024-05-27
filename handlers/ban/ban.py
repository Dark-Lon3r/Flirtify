from loader import bot, CallbackQuery, Message, dp, types

from keyboards.keyboards import Admin, InlineKeyboardButton, InlineKeyboardMarkup
from userdata.func_sql import get_user_info
from imports import aiosqlite


async def ban_user_func(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        # Добавление пользователя в таблицу "ban"
        await db.execute("INSERT INTO ban (id) VALUES (?)", (user_id,))
        
        # Удаление данных из таблицы "anketa" для данного пользователя
        await db.execute("DELETE FROM anketa WHERE id = ?", (user_id,))
        await db.execute("DELETE FROM rating WHERE id = ?", (user_id,))
        
        result = await db.execute("SELECT COUNT(*) FROM shown_profiles WHERE user_id = ? AND profile_id = ?", (user_id, user_id, ))
        if result is not None:
            await db.execute("DELETE FROM shown_profiles WHERE user_id = ? AND profile_id = ?", (user_id, user_id, ))

        await db.execute("DELETE FROM complaints WHERE id = ?", (user_id,))
        
        await db.commit()

async def no_ban_user_func(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        await db.execute("UPDATE complaints SET value_complaints = ?, send_complaints_id = ?, send_complaints_username = ?, send_complaints_catigories = ? WHERE id = ?", (int(0), int(0), int(0), int(0), user_id, ))
        await db.commit()


@dp.callback_query_handler(lambda c: c.data == 'key_ban')
async def key_ban_logic(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id - 2)
