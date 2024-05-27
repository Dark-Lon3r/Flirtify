from loader import bot, dp, CallbackQuery, Message
from editor_photo import add_text_to_photo

from keyboards.keyboards import Floor, Ancketa_main, Hobbies
from userdata.func_sql import add_user
from locales.translate import translate_start

from imports import FSMContext, State, StatesGroup, ContentType
from imports import Nominatim, Location, os, asyncio


class CreateAncketStates(StatesGroup):
    NAME = State()
    AGE = State()
    GENDER = State()
    SEARCH_GENDER= State()
    DESCRIPTION = State()
    HOBBIES = State()
    LOCATION = State()
    LOCATION_INPUT = State()
    LOCATION_SEARCH = State()
    PHOTO = State()


@dp.callback_query_handler(lambda c: c.data == 'create_ancket')
async def ancketa_create_user(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "<i>Я завжди вірю в перше враження, тож давай знайомитись: я Flirtify, а ти?😇</i>")
    await CreateAncketStates.NAME.set()


@dp.message_handler(state=CreateAncketStates.NAME)
async def process_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if len(message.text) >= 2:
            data['name'] = message.text
            data['username'] = message.from_user.username

            await message.answer("<i>Як кажуть, вік – це лише число. Але для нашого проекту вік може бути ключовим фактором! 😏🔑</i>")
            await CreateAncketStates.AGE.set()
            await message.delete()
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

        else:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await bot.send_message(message.from_user.id, "<i>Я помітив, що у тебе таке коротке ім'я, лише 1 символ? 🤔 Не жартуй, давай напиши нормально, давай додамо ще трохи буквочок у це вибухове поєднання! 💥😉</i>")            

@dp.message_handler(state=CreateAncketStates.AGE)
async def process_age(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isdigit():
            await bot.send_message(message.from_user.id, "<i>Я розумію, що літери можуть бути дуже привабливими, але в цьому випадку цифри були б доречнішими 🤔😉</i>")
		
        else:
            age = int(message.text)
            if 14 <= age <= 45:
                data['age'] = str(age)

                menu = Floor()
        	    
                await message.answer("<i>Ми просто хочемо знати, з ким маємо справу: мачо чи принцеса?💪👸</i>", reply_markup = await menu.get_menu_keyboard())
                await CreateAncketStates.GENDER.set()
                await message.delete()
                await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)

            else:
                await bot.send_message(message.from_user.id, "<i>Від 14 до 45 років – межі нашого бот-тусовника! 🎉</i>")


@dp.callback_query_handler(state=CreateAncketStates.GENDER)
async def process_gender(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = callback_query.data

        menu = Floor()
        await callback_query.message.edit_text("🔍 Хочеш, щоб я розкрив твої уподобання? Розкажи мені, яка стать тобі потрібна, і я зроблю все можливе! 😏", reply_markup = await menu.get_menu_keyboard())
        await CreateAncketStates.SEARCH_GENDER.set()


@dp.callback_query_handler(state=CreateAncketStates.SEARCH_GENDER)
async def search_gender(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['search_gender'] = callback_query.data

        await bot.send_message(callback_query.from_user.id, "<i>Мені здається, ви дуже цікава особа. Давайте заповнимо опис, щоб я був у цьому впевнений 😄📝</i>")
        await callback_query.message.delete()
        await CreateAncketStates.DESCRIPTION.set()


@dp.message_handler(state=CreateAncketStates.DESCRIPTION)
async def process_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

        hobbies = Hobbies()
        await bot.send_message(message.from_user.id, "<i>Я чув, що хобі - це те, що ти робиш із задоволенням, навіть якщо ніхто не дивиться. \nТо що, яке твоє хобі? 😉</i>", reply_markup = await hobbies.get_menu_hobbies_choose())
        await message.delete()
        await CreateAncketStates.HOBBIES.set()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)



# Обработчик выбора категории хобби
@dp.callback_query_handler(lambda query: query.data.startswith('category_'), state=CreateAncketStates.HOBBIES)
async def process_hobby_category(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)

    category = callback_query.data.split('_')[1]
    hobbies = Hobbies()
    # В зависимости от выбранной категории, отправляем соответствующее меню с хобби
    if category == 'it':
        await callback_query.message.edit_text("<i>👾 Ого, вже знаходишся в категорії IT/Технології! Я впевнений, ти знайдеш тут щось цікаве, так само як і мене 😉💻</i>", reply_markup= await hobbies.get_menu_hobbies_it())
    elif category == 'sport':
        await callback_query.message.edit_text("<i>🔥 Вибери своє спортивне хобі! Чи знаєш, що спорт піднімає не тільки настрій, але й температуру? 😏 Обери спорт, який тобі до вподоби, і ми знайдемо тобі співрозмовника, з яким ти зможеш спалити зайві калорії! 💪🔥</i>", reply_markup= await hobbies.get_menu_hobbies_sport())
    elif category == 'cooking':
        await callback_query.message.edit_text("<i>🍳 Ой, оскільки ми розмовляємо про кулінарію, дозволь мені розпалити твої кулінарні фантазії! 😏🔥 Обери кулінарний шлях, а я покажу тобі, що подібність в смаках може призвести до неймовірного зв'язку! 💕</i>", reply_markup= await hobbies.get_menu_hobbies_cooking())
    elif category == 'creativity':
        await callback_query.message.edit_text("<i>🎨 Ох, ми дійшли до категорії Творчість та Мистецтво! Тут наше спілкування може стати справжнім мистецтвом, а твоя креативність зацікавить мене ще більше! 😏💫</i>", reply_markup= await hobbies.get_menu_hobbies_creativity())
    elif category == 'back':
        await callback_query.message.edit_text("<i>Я чув, що хобі - це те, що ти робиш із задоволенням, навіть якщо ніхто не дивиться. \nТо що, яке твоє хобі? 😉</i>", reply_markup = await hobbies.get_menu_hobbies_choose())

    # Сохраняем выбранную категорию в состоянии
    async with state.proxy() as data:
        data['category'] = category


# Обработчик выбора конкретного хобби
@dp.callback_query_handler(lambda query: query.data.startswith('hobby_'), state=CreateAncketStates.HOBBIES)
async def process_hobby_selection(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    hobby = callback_query.data.split('_')[1]
    # Получаем выбранную категорию из состояния
    async with state.proxy() as data:
        data['hobby'] = hobby

    ancketa_main = Ancketa_main("uk")
    await callback_query.message.edit_text("<i>🌍 Мандрівник, як ми дізнаємося, де ти? Вибирай:\n 1)Автоматично за допомогою GPS \n2)Чи вручну! 🗺️🔍</i>", reply_markup = await ancketa_main.get_menu_choice_location())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('btn1', 'btn2')), state=CreateAncketStates.HOBBIES)
async def choice_location(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=callback_query.id)
    if callback_query.data.startswith("btn1"):
        await callback_query.message.delete()

        key_location = Ancketa_main("uk")
        
        await bot.send_message(callback_query.from_user.id, "<i>🌍 Активуй свій GPS-приймач і тисни кнопку нижче, щоб ми знайшли тебе! 📍🛰️</i>", reply_markup = await key_location.get_menu_keyboard_ancketa_location())
        await CreateAncketStates.LOCATION.set()

    elif callback_query.data.startswith("btn2"):
        await callback_query.message.delete()

        await bot.send_message(callback_query.from_user.id, "<i>🏙️ Ти наш супергеограф! Введи своє місто самостійно і дай нам знати, де тебе можна зустріти на романтичний поцілунок! 😘🌆</i>")
        await CreateAncketStates.LOCATION_INPUT.set()


@dp.message_handler(content_types=[ContentType.LOCATION], state=CreateAncketStates.LOCATION)
async def process_location(message: Message, state: FSMContext):
    location = message.location
    async with state.proxy() as data:
        if 'location' in data and data['location'] is not None:
            data['location'].latitude = location.latitude
            data['location'].longitude = location.longitude
        else:
            data['location'] = Location(latitude=location.latitude, longitude=location.longitude)

        geolocator = Nominatim(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        location_info = geolocator.reverse(f"{location.latitude}, {location.longitude}", exactly_one=True, timeout=10)
        location_send_info = location_info.raw.get('address', {}).get('city', 'Неизвестно')
        data['location'] = location_send_info

        if location_send_info == 'Неизвестно':
            await bot.send_message(message.from_user.id, 'Хм, не вдалося визначити твоє місцезнаходження, тому, введи його нижче')
            await CreateAncketStates.LOCATION_INPUT.set()

        else:
            await bot.send_message(message.chat.id, "<i>Хм, яке місто ви хотіли б дослідити у пошуках нових людей?🌃😏</i>")
            await CreateAncketStates.LOCATION_SEARCH.set()
            await message.delete()
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)


@dp.message_handler(state=CreateAncketStates.LOCATION_INPUT)
async def process_location_input(message: Message, state: FSMContext):
    async with state.proxy() as data:
        location_text = message.text

        # Проверяем наличие буквы "ы" в строке и заменяем её на "и"
        if 'ы' in location_text:
            location_text = location_text.replace('ы', 'и')

        data['location'] = location_text  # сохраняем измененную строку в переменную

    await bot.send_message(message.from_user.id, "<i>На яке місто ми поїдемо шукати вам нових знайомих? 🤗🏙️</i>")
    await CreateAncketStates.LOCATION_SEARCH.set()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)


@dp.message_handler(state=CreateAncketStates.LOCATION_SEARCH)
async def process_location_search(message: Message, state: FSMContext):
    async with state.proxy() as data:
        location_search = message.text

        # Проверяем наличие буквы "ы" в строке и заменяем её на "и"
        if 'ы' in location_search:
            location_search = location_search.replace('ы', 'и')

        data['location_search'] = location_search  # сохраняем измененную строку в переменную

    await bot.send_message(message.from_user.id, "<i>Швидше за все, ти найкрасивіша людина у світі, але нам потрібно переконатися. Надсилай своє фото!🤩</i>")
    await CreateAncketStates.PHOTO.set()
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)


# Обработчик для сохранения фото
@dp.message_handler(state=CreateAncketStates.PHOTO, content_types=['photo'])
async def process_photo(message: Message, state: FSMContext):
    # Получаем id пользователя и id фото
    user_id = message.from_user.id
    
    photo_id = message.photo[-1].file_id
    photo = await bot.get_file(photo_id)
    
    # Получаем расширение файла из file_path
    file_extension = os.path.splitext(photo.file_path)[-1]
    
    photo_path = os.path.join("photo_users", f"{user_id}{file_extension}")
    await photo.download(destination_file=photo_path)
        
    async with state.proxy() as data:
        data['photo'] = photo_id
        data['photo_path'] = photo_path
        await save_user_data(user_id, data)
        await state.finish()
        await message.delete()
        await bot.delete_message(message.chat.id, message.message_id - 1)


async def save_user_data(user_id, data):
    try:
        loop = asyncio.get_event_loop()
        task = loop.create_task(add_text_to_photo(data.get('photo_path'), ))
        await task

        photo = task.result()

        if photo:
            # Получаем данные из состояния
            name = data.get('name')
            username = data['username']
            age = data.get('age')
            gender = data.get('gender')
            search_gender = data.get('search_gender')
            description = data.get('description')
            hobbies = data.get('hobby')
            location = data.get('location')
            location_search = data.get('location_search')
            photo_path = photo
            languages = "uk"

            loop = asyncio.get_event_loop()
            task = loop.create_task(add_user(user_id, username, name, age, gender, search_gender, description, hobbies, location, location_search, photo_path,languages, ))
            await task

    except Exception as e:
        print(e)

    finally:
        # Заканчиваем состояние
        menu_ancketa = Ancketa_main("uk")
        await bot.send_message(user_id, "<i>Ура! Ваша анкета створена та готова до підкорення сердець!❤️😉</i>", reply_markup = await menu_ancketa.get_menu_keyboard_ancketa())
        