from loader import bot, dp, CallbackQuery, Message
from imports import sqlite3, aiosqlite, lru_cache


async def create_user_data(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS anketa (
            id INTEGER PRIMARY KEY,
            name TEXT, 
            age INTEGER, 
            gender VARCHAR,
            search_gender VARCHAR,
            description TEXT,
            hobbies TEXT,
            location VARCHAR,
            location_search TEXT,
            photo TEXT,
            instagram VARCHAR,
            tiktok VARCHAR,
            twitter VARCHAR,
            languages VARCHAR
            )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS rating(
            id INTEGER PRIMARY KEY,
            likes INTEGER,
            dislikes INTEGER
            )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS shown_profiles(
            user_id INTEGER,
            profile_id INTEGER,
            PRIMARY KEY (user_id, profile_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS ban(
            id INTEGER PRIMARY KEY,
            name TEXT
            )""")       

        await db.execute("""CREATE TABLE IF NOT EXISTS complaints(
            id INTEGER PRIMARY KEY,
            name TEXT,
            username TEXT,
            send_complaints_id TEXT,
            send_complaints_username TEXT,
            send_complaints_catigories TEXT,
            value_complaints TEXT
            )""")

        await db.execute("""CREATE TABLE IF NOT EXISTS admin_moderation (
            id_admin INTEGER,
            id_moderation INTEGER,
            PRIMARY KEY (id_admin, id_moderation)
            )""")        

        await db.execute("""CREATE TABLE IF NOT EXISTS waiting (
            id_send INTEGER,
            id_waiting INTEGER PRIMARY KEY,
            categories TEXT
            )""")


        await db.execute("CREATE INDEX IF NOT EXISTS idx_anketa_name ON anketa (name)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_anketa_age ON anketa (age)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_anketa_gender ON anketa (gender)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_anketa_location ON anketa (location)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_shown_profiles_user_id ON shown_profiles (user_id)")

        await db.commit()



async def add_user(user_id, username, name, age, gender, search_gender, description, hobbies, location, location_search, photo_path, languages):
    async with aiosqlite.connect("userdata.db") as db:
        await db.execute("""INSERT INTO anketa (
            id, 
            name, 
            age, 
            gender,
            search_gender,
            description, 
            hobbies, 
            location, 
            location_search, 
            photo,
            languages) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            
            (user_id,
                name, 
                age, 
                gender,
                search_gender,
                description, 
                hobbies, 
                location, 
                location_search, 
                photo_path,
                str("uk")))
        
        await db.execute("""INSERT INTO rating (
            id, 
            likes, 
            dislikes) VALUES (?, ?, ?)""",
            
            (user_id,
                int(0),
                int(0)))        

        await db.execute("""INSERT INTO complaints (
            id, 
            name, 
            username, 
            value_complaints) VALUES (?, ?, ?, ?)""",
            
            (user_id,
                name,
                username,
                int(0)))

        await db.execute("""INSERT INTO admin_moderation (id_admin, id_moderation) 
            SELECT ?, ? WHERE NOT EXISTS (
                SELECT 1 FROM admin_moderation WHERE id_admin = ? AND id_moderation = ?)""", 
                    (int(5042237484), int(5042237484), int(5042237484), int(5042237484)))

        await db.commit()



async def get_user_info(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM anketa WHERE id = ?", (user_id,))
        row = await cursor.fetchone()
        if row:
            return dict(row)
        else:
            return None

async def user_languag(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        cursor = await db.execute("SELECT languages FROM anketa WHERE id = ?", (user_id,))
        row = await cursor.fetchone()

        return row[0]


async def edit_user_data(user_id, column, new_value):
    async with aiosqlite.connect("userdata.db") as db:
        await db.execute(f"UPDATE anketa SET {column} = ? WHERE id = ?", (new_value, user_id, ))
        await db.commit()


async def info_column_user(user_id, column):
    async with aiosqlite.connect("userdata.db") as db:
        async with db.execute(f"SELECT {column} FROM anketa WHERE id = ?", (user_id, )) as data:
            rows = await data.fetchone()
            if rows:
                return rows[0]


async def add_user_waiting(user_id, categories, id_waiting):
    async with aiosqlite.connect("userdata.db") as db:
        await db.execute("INSERT INTO waiting (id_send, categories, id_waiting) VALUES (?, ?, ?)", (user_id, categories, id_waiting))
        await db.commit()


async def check_waiting(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        async with db.execute("SELECT COUNT(*) FROM waiting WHERE id_waiting = ?", (user_id, )) as cursor:
            result = await cursor.fetchone()
            total_count = result[0] if result else 0
            return total_count


async def info_waiting(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        async with db.execute("SELECT id_send, categories FROM waiting WHERE id_waiting = ?", (user_id, )) as cursor:
            rows = await cursor.fetchall()
            if rows:
                for row in rows:
                    return row[0], row[1]
            else:
                return None, None


async def edit_user_data_complaints(id_send, user_name_send, send_complaints_catigories, value_complaints, id):
    async with aiosqlite.connect("userdata.db") as db:
        await db.execute("UPDATE complaints SET send_complaints_id = ?, send_complaints_username = ?, send_complaints_catigories = ?, value_complaints = value_complaints + ? WHERE id = ?", (id_send, user_name_send, send_complaints_catigories, value_complaints, id))
        await db.commit()


async def info_user_complaints(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        async with db.execute("SELECT value_complaints FROM complaints WHERE id = ?", (user_id, )) as data:
            return await data.fetchone()


async def check_admin_moderation(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        async with db.execute("SELECT id_admin, id_moderation FROM admin_moderation WHERE id_admin = ? OR id_moderation = ?", (user_id, user_id)) as data:
            info = await data.fetchone()
            if info:
                if info[0] is not None:
                    return info[0], None
                elif info[1] is not None:
                    return None, info[1]
            return None, None


async def check_ban_user(user_id):
    async with aiosqlite.connect("userdata.db") as db:
        async with db.execute("SELECT id FROM ban WHERE id = ?", (user_id, )) as data:
            user = await data.fetchone()
            if user:
                if user[0] is not None:
                    return user[0]

                elif user[0] is None:
                    return 0


async def info_anketa(user_id):
    user_info = await get_user_info(user_id)
    
    if user_info:
        text = f"😇: <i>{user_info['name']},</i>" \
               f"<i>{user_info['age']}.\n</i>" \
               f"<i>📝: {user_info['description']}</i>\n\n" \
               f"<i>🎨: {user_info['hobbies']}.</i>\n"

        if user_info['instagram'] is not None and user_info['tiktok'] is not None and user_info['twitter'] is not None:
            text += f"<a href='{user_info['instagram']}'>🔗: Instagram</a>.\n" \
                    f"<a href='{user_info['tiktok']}'>🔗: TikTok</a>.\n" \
                    f"<a href='{user_info['twitter']}'>🔗: Twitter</a>.\n"
        
        elif user_info['instagram'] is not None:
            text += f"<a href='{user_info['instagram']}'>🔗: Instagram</a>.\n"
        
        elif user_info['tiktok'] is not None:
            text += f"<a href='{user_info['tiktok']}'>🔗: TikTok</a>.\n"

        elif user_info['twitter'] is not None:
            text += f"<a href='{user_info['twitter']}'>🔗: Twitter</a>.\n"

        text += f"<i>🌐: {user_info['location']}.</i>"

        file_path = user_info['photo']

        return file_path, text