from loader import bot, dp, types, CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from locales.translate import translate
from keyboards.keyboards import Pay, InlineKeyboardMarkup, InlineKeyboardButton
import paypalrestsdk


paypal_key = Pay()

# настройки PayPal
paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": "",
  "client_secret": ""
})


@dp.callback_query_handler(lambda c: c.data == 'paypal')
async def paypal_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(await translate(callback_query.from_user.id, "paypal_info"), reply_markup = await paypal_key.get_menu_paypal())


@dp.callback_query_handler(lambda c: c.data.startswith('price_'))
async def buy_handler(callback_query: types.CallbackQuery, state: FSMContext):
    price_data = callback_query.data.split('_')
    if len(price_data) > 1:
        price = price_data[1]
        # Продолжайте выполнение кода с выбранной ценой
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "https://t.me/Flirt_ify_bot",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Підримка💰",
                        "sku": "item",
                        "price": price,
                        "currency": "USD",
                        "quantity": 1
                        }]},
                
                "amount": {
                    "total": price,
                    "currency": "USD"},
                "description": "Підримка💰"}]
        })
    
    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                # отправка ссылки на страницу оплаты PayPal
                url_paypal = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
                url_paypal.add(
                    InlineKeyboardButton('💸', url = redirect_url),
                    InlineKeyboardButton('⬅️', callback_data='back')
                )
                await callback_query.message.edit_text('💸💸', reply_markup = url_paypal)
    else:
        await callback_query.message.edit_text(await translate(callback_query.from_user.id, "error_paypal_create"), reply_markup = await paypal_key.get_menu_donate())
