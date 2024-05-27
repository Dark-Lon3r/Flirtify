from loader import dp, bot, types, Message, CallbackQuery
from imports import json, sqlite3, aiosqlite, asyncio, cache


async def translate(user_id: int, key):
    async with aiosqlite.connect("userdata.db") as db:
        async with db.execute('SELECT languages FROM anketa WHERE id = ?', (user_id, )) as cursor:
            lang = await cursor.fetchone()
            
            # загружаем файл локализации для выбранного языка
            with open("locales/translations.json", 'r') as f:
                translations = json.load(f)

            # возвращаем перевод
            return translations[key][lang[0]]

@cache
async def translate_start(lang, key):
    with open("locales/translations.json", 'r') as f:
        translations = json.load(f)
    return translations[key][lang]


def translate_key(lang):
    with open("locales/translations.json", 'r') as f:
        translations = json.load(f)
    return translations