from loader import bot, CallbackQuery, Message, dp, types

from keyboards.keyboards import Admin
from userdata.func_sql import check_admin_moderation

from imports import aiosqlite


admin_key = Admin()



async def get_total_users_count():
    async with aiosqlite.connect("userdata.db") as db:
        query = "SELECT COUNT(*) FROM anketa"
        async with db.execute(query) as cursor:
            result = await cursor.fetchone()
            total_count = result[0] if result else 0
            return total_count


async def admin_func(callback_query: CallbackQuery):
    total_user = await get_total_users_count()
    await callback_query.message.edit_text(f"Привет, Админ. \n\nВсего пользователей {total_user}", reply_markup = await admin_key.get_admin_menu())