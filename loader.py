from imports import Bot, Dispatcher, types, executor, asyncio, set_default_commands, logging, MemoryStorage, CallbackQuery, Message, multiprocessing


TOKEN = "6115569749:AAF8VwSYiVgsKqa1IPYy8K0lwFoYBOig2bI"

bot = Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)

logging.basicConfig(level=logging.WARNING)


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


if __name__ == "__main__":
    from allHandlers import dp  # Импорт dp после определения middleware
    multiprocessing.Process(target=executor.start_polling(dp, on_startup=on_startup, skip_updates=True)).start()