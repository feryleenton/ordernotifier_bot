from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton('Добавить \ Обновить Ozon API Key'),
        KeyboardButton('Добавить \ Обновить Wildberries API Key')
    ],
    [
        KeyboardButton('Отписаться'),
    ]

], resize_keyboard=True)
