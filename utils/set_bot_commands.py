from imports import types


async def set_default_commands(dp):
	""" Установка дефолтных команд """
	await dp.bot.set_my_commands(
		[
			types.BotCommand("start", "Запустить"),
			types.BotCommand("help", "Помощь"),
			types.BotCommand("menu", "Меню")
		]
	)
