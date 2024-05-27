from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from imports import Location, json, asyncio
from locales.translate import translate_start, translate_key
from imports import cache


class Menu:
    def __init__(self):
        self.menu_keyboard = InlineKeyboardMarkup(row_width=2)
        self.menu_keyboard.add(
            InlineKeyboardButton('🏹', callback_data='create_ancket')
        )

    async def get_menu_keyboard_start(self):
        return self.menu_keyboard


class Floor:
    def __init__(self):
        self.floor_keyboard = InlineKeyboardMarkup(row_width=2)
        self.floor_keyboard.add(
            InlineKeyboardButton('💪Мачо', callback_data='Male'),
            InlineKeyboardButton('👸Принцеса', callback_data='Female')
        )

    async def get_menu_keyboard(self):
        return self.floor_keyboard


class Hobbies:
    def __init__(self):
        self.menu_hobbies_choose = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
        self.menu_hobbies_choose.add(
            InlineKeyboardButton('Група IT 👾', callback_data='category_it'),
            InlineKeyboardButton('Спорт ⚽️', callback_data='category_sport'),
            InlineKeyboardButton('Кулінарія 🍳', callback_data='category_cooking'),
            InlineKeyboardButton('Творчість та Мистецтво 🎨', callback_data='category_creativity'),
        )

        self.menu_hobbies_it = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.menu_hobbies_it.add(
            InlineKeyboardButton('Програмування, розробка веб-сайтів 💻', callback_data='hobby_Програмування'),
            InlineKeyboardButton('Створення мобільних додатків 📱', callback_data='hobby_Створення_мобільних_додатків'),
            InlineKeyboardButton("Кіберспорт та комп'ютерні ігри 🎮", callback_data='hobby_Кіберспорт'),
            InlineKeyboardButton('3D-графіка 🖥️', callback_data='hobby_3D-графіка'),
            InlineKeyboardButton('Розробка програмного забезпечення 🛠️', callback_data='hobby_Розробка-ПО'),
            InlineKeyboardButton('Криптографія та кібербезпека 🔒', callback_data='hobby_Кібербезпека'),
            InlineKeyboardButton('⬅️', callback_data='category_back')
        )

        self.menu_hobbies_sport = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.menu_hobbies_sport.add(
            InlineKeyboardButton('Футбол ⚽️', callback_data='hobby_Футбол'),
            InlineKeyboardButton('Баскетбол 🏀', callback_data='hobby_Баскетбол'),
            InlineKeyboardButton("Теніс 🎾", callback_data='hobby_Теніс'),
            InlineKeyboardButton('Біг 🏃', callback_data='hobby_Біг'),
            InlineKeyboardButton('Боротьба 🤼', callback_data='hobby_Боротьба'),
            InlineKeyboardButton('Бокс 🥊', callback_data='hobby_Бокс'),
            InlineKeyboardButton('⬅️', callback_data='category_back')
        )

        self.menu_hobbies_cooking = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.menu_hobbies_cooking.add(
            InlineKeyboardButton('Випічка та кондитерське мистецтво 🍰', callback_data='hobby_Кондитерське_мистецтво'),
            InlineKeyboardButton('Прикраса тортів та десертів 🎂', callback_data='hobby_Прикраса_тортів'),
            InlineKeyboardButton("Готування на грилі та барбекю 🍗", callback_data='hobby_Готування_на_грилі'),
            InlineKeyboardButton('⬅️', callback_data='category_back')
        )

        self.menu_hobbies_creativity = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.menu_hobbies_creativity.add(
            InlineKeyboardButton('Малювання та живопис 🎨', callback_data='hobby_Малювання'),
            InlineKeyboardButton('Фотографія та відеозйомка 📷', callback_data='hobby_Фотографія'),
            InlineKeyboardButton("Музика та гра на інструментах 🎵", callback_data='hobby_Музика'),
            InlineKeyboardButton("Вокал та спів 🎤", callback_data='hobby_Вокал'),
            InlineKeyboardButton("Танці та хореографія 💃", callback_data='hobby_Танці'),
            InlineKeyboardButton("Театр та акторська майстерність 🎭", callback_data='hobby_Театр'),
            InlineKeyboardButton("Дизайн інтер'єру та декорування 🏠", callback_data='hobby_Дизайн'),
            InlineKeyboardButton("Скульптура та різьблення по дереву 🪵", callback_data='hobby_Скульптура'),
            InlineKeyboardButton('⬅️', callback_data='category_back')
        )

    async def get_menu_hobbies_choose(self):
        return self.menu_hobbies_choose

    async def get_menu_hobbies_it(self):
        return self.menu_hobbies_it

    async def get_menu_hobbies_sport(self):
        return self.menu_hobbies_sport

    async def get_menu_hobbies_cooking(self):
        return self.menu_hobbies_cooking

    async def get_menu_hobbies_creativity(self):
        return self.menu_hobbies_creativity


class Ancketa_main:
    def __init__(self, lang):
        self.lang = lang
        self.translations = translate_key(lang)

        self.ancketa_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.ancketa_keyboard.add(
            InlineKeyboardButton(self.translations['my_ancket'][self.lang], callback_data='my_ancketa'),
            InlineKeyboardButton(self.translations['search_ancket'][self.lang], callback_data='start_ancket'),
            InlineKeyboardButton('🛎', callback_data='status_notification'),
            InlineKeyboardButton(self.translations['settings'][self.lang], callback_data='settings'),
            InlineKeyboardButton(self.translations['support'][self.lang], callback_data='donate')
        )

        self.ancketa_choice_judging = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.ancketa_choice_judging.add(
            InlineKeyboardButton(self.translations['my_ancket'][self.lang], callback_data='my_ancketa'),
            InlineKeyboardButton(self.translations['search_ancket'][self.lang], callback_data='start_ancket'),
            InlineKeyboardButton('🛎', callback_data='status_notification'),
            InlineKeyboardButton(self.translations['settings'][self.lang], callback_data='settings'),
            InlineKeyboardButton('😈Таємниць суддів', callback_data='judging'),
            InlineKeyboardButton(self.translations['support'][self.lang], callback_data='donate')
        )

        self.ancketa_keyboard_location = ReplyKeyboardMarkup(resize_keyboard=True)
        self.ancketa_keyboard_location.add(
            KeyboardButton('🌐Надіслати місцезнаходження', request_location=True),
        )

        self.ancketa_choice_location = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.ancketa_choice_location.add(
            InlineKeyboardButton('1️⃣', callback_data='btn1'),
            InlineKeyboardButton('2️⃣', callback_data='btn2')
        )

        self.ancketa_choice_location_edit = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.ancketa_choice_location_edit.add(
            InlineKeyboardButton('1️⃣', callback_data='btn1_edit'),
            InlineKeyboardButton('2️⃣', callback_data='btn2_edit')
        )

        self.ancketa_tackle = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.ancketa_tackle.add(
            InlineKeyboardButton('▶️', callback_data='start_generate'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

    async def get_menu_keyboard_ancketa(self):
        return self.ancketa_keyboard    

    async def get_menu_judging(self):
        return self.ancketa_choice_judging    

    async def get_menu_keyboard_ancketa_location(self):
        return self.ancketa_keyboard_location

    async def get_menu_choice_location(self):
        return self.ancketa_choice_location

    async def get_menu_choice_location_edit(self):
        return self.ancketa_choice_location_edit

    async def get_menu_ancketa_tackle(self):
        return self.ancketa_tackle


class Settings:
    def __init__(self, lang):
        self.lang = lang
        self.translations = translate_key(lang)
        
        self.settings_keyboard_choice_ancketa = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.settings_keyboard_choice_ancketa.add(
            InlineKeyboardButton(self.translations['search'][self.lang], callback_data='search_settings'),
            InlineKeyboardButton(self.translations['settings_ancketa'][self.lang], callback_data='settings_ancketa'),
            InlineKeyboardButton(self.translations['social'][self.lang], callback_data='social'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        self.settings_keyboard_search = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.settings_keyboard_search.add(
            InlineKeyboardButton(self.translations['edit_search_gender'][self.lang], callback_data='edit_search_gender'),
            InlineKeyboardButton(self.translations['edit_search_location'][self.lang], callback_data='edit_search_location'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        self.settings_ancketa_social = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.settings_ancketa_social.add(
            InlineKeyboardButton(self.translations['add_instagram'][self.lang], callback_data='add_instagram'),
            InlineKeyboardButton(self.translations['add_tiktok'][self.lang], callback_data='add_tiktok'),
            InlineKeyboardButton(self.translations['add_twitter'][self.lang], callback_data='add_twitter'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        self.settings_key_anketa = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.settings_key_anketa.add(
            InlineKeyboardButton(self.translations['edit_location'][self.lang], callback_data='edit_location'),
            InlineKeyboardButton(self.translations['edit_age'][self.lang], callback_data='edit_age'),
            InlineKeyboardButton(self.translations['edit_name'][self.lang], callback_data='edit_name'),
            InlineKeyboardButton(self.translations['edit_photo'][self.lang], callback_data='edit_photo'),
            InlineKeyboardButton(self.translations['edit_description'][self.lang], callback_data='edit_description'),
            InlineKeyboardButton(self.translations['edit_hobbies'][self.lang], callback_data='edit_hobbies'),
            InlineKeyboardButton(self.translations['edit_languages'][self.lang], callback_data='edit_languages'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        self.languages_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.languages_keyboard.add(
            InlineKeyboardButton('🇺🇦', callback_data='uk_lang'),
            InlineKeyboardButton('ru', callback_data='ru_lang')
        )

        self.cancel_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.cancel_keyboard.add(
            InlineKeyboardButton('❌', callback_data='cancel')
        )

        self.back_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.back_keyboard.add(
            InlineKeyboardButton('⬅️', callback_data='back')
        )


    async def keyboard_choice_ancketa(self):
        return self.settings_keyboard_choice_ancketa

    async def settings_search(self):
        return self.settings_keyboard_search

    async def settings_social(self):
        return self.settings_ancketa_social

    async def get_menu_settings_anketa(self):
        return self.settings_key_anketa

    async def get_menu_keyboard_languages(self):
        return self.languages_keyboard

    async def get_menu_cancel(self):
        return self.cancel_keyboard

    async def get_menu_back(self):
        return self.back_keyboard

@cache
class Pay:
    def __init__(self):
        self.donate_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
        self.donate_keyboard.add(
            InlineKeyboardButton('🥰MONOBANK', callback_data="monobank"),
            InlineKeyboardButton('💸PayPal', callback_data="paypal"),
            InlineKeyboardButton('📜Patreon', url="https://patreon.com/Flirtify"),
            InlineKeyboardButton('📧Gmail', callback_data="gmail_send"),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        self.paypal_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
        self.paypal_keyboard.add(
            InlineKeyboardButton('1000UAH', callback_data='price_27.16'),
            InlineKeyboardButton('500UAH', callback_data='price_13.58'),
            InlineKeyboardButton('200UAH', callback_data='price_5.43'),
            InlineKeyboardButton('150UAH', callback_data='price_4.07'),
            InlineKeyboardButton('100UAH', callback_data='price_2.72'),
            InlineKeyboardButton('50UAH', callback_data='price_1.36'),
            InlineKeyboardButton('⬅️', callback_data='back')
        )

        self.monobank_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.monobank_keyboard.add(
            InlineKeyboardButton('🥰MONOBANK', url="https://send.monobank.ua/jar/9Mp2muNXj1"),
            InlineKeyboardButton('⬅️', callback_data='back')
        )


    async def get_menu_donate(self):
        return self.donate_keyboard


    async def get_menu_paypal(self):
        return self.paypal_keyboard


    async def get_menu_monobank(self):
        return self.monobank_keyboard


class Admin:
    def __init__(self):
        self.admin_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        self.admin_keyboard.add(
            InlineKeyboardButton('🔄Очистить таблицу скрытых', callback_data='clean_shown'),
            InlineKeyboardButton('📣Рассылка', callback_data='send_users_sms'),
            InlineKeyboardButton('📥Отправить смс пользователю', callback_data='send_sms_user'),
            InlineKeyboardButton('💔Забанить пользователя', callback_data='ban_user'),
            InlineKeyboardButton('➕Добавить модератора', callback_data='add_moderation'),
            InlineKeyboardButton('➖Удалить модератора', callback_data='delete_moderation'),
            InlineKeyboardButton('🔒Удалить бан пользователю', callback_data='delete_ban_user'),
            InlineKeyboardButton('↩️Выйти с админки', callback_data='exit_admin_menu')
        )

        self.admin_key_cancel = InlineKeyboardMarkup(row_width=1, inline_keyboard=True)
        self.admin_key_cancel.add(
            InlineKeyboardButton('❌', callback_data='cancel_admin')
        )        

        self.moderation_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=True)
        self.moderation_menu.add(
            InlineKeyboardButton('📝Список скарг', callback_data='list_complaints'),
            InlineKeyboardButton('❌', callback_data='cancel')
        )        

        self.moderation_menu_choice = InlineKeyboardMarkup(row_width=1, inline_keyboard=True)
        self.moderation_menu_choice.add(
            InlineKeyboardButton('💔Забанить пользователя', callback_data='ban_user'),
            InlineKeyboardButton('💞Простить', callback_data='no_ban_user'),
            InlineKeyboardButton('❌', callback_data='cancel')
        )


    async def get_admin_menu(self):
        return self.admin_keyboard    

    async def get_moderation_menu(self):
        return self.moderation_menu

    async def get_moderation_ban(self):
        return self.moderation_menu_choice

    async def get_admin_menu_cancel(self):
        return self.admin_key_cancel