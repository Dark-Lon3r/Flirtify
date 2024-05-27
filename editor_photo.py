from imports import asyncio, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from userdata.func_sql import info_column_user


async def add_text_to_photo(photo):
	if photo:
		# Загрузка изображения
		image = Image.open(photo)

		# Загрузка водяного знака
		watermark_text = 'Flirtify'
		font_path = 'font_bot/Disket-Mono-Regular.ttf'  # Путь к шрифту, который будет использоваться для водяного знака
		font_size = 15
		opacity = 0.5  # Прозрачность водяного знака (от 0 до 1)

		image = image.filter(ImageFilter.SHARPEN)

	    # Настройка яркости и контраста
		enhancer = ImageEnhance.Brightness(image)
		image = enhancer.enhance(0.8)  # Уменьшение яркости на 20%

		enhancer = ImageEnhance.Contrast(image)
		image = enhancer.enhance(1.1)

		enhancer = ImageEnhance.Color(image)
		image = enhancer.enhance(1.1)
		image = image.filter(ImageFilter.GaussianBlur(radius=0.3))

		enhancer = ImageEnhance.Sharpness(image)
		image = enhancer.enhance(0.2)
		image = ImageOps.autocontrast(image)

		# Создание объекта для рисования на изображении
		draw = ImageDraw.Draw(image)

		# Создание объекта шрифта
		font = ImageFont.truetype(font_path, font_size)

		# Определение размеров водяного знака
		watermark_text_width, watermark_text_height = draw.textsize(watermark_text, font=font)

		# Расчет координат для размещения водяного знака (в данном случае, внизу слева)
		position = (10, image.height - watermark_text_height - 10)

		# Рисование водяного знака
		draw.text(position, watermark_text, font=font, fill=(255, 255, 255, int(255 * opacity)))

		# Сохранение изображения с водяным знаком
		output_image_path = photo
		image.save(output_image_path)

		return photo