from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/add_joke")],
        [KeyboardButton(text="/send_custom_message")],
    ],
    resize_keyboard=True,
)

user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="/stop")],
    ],
    resize_keyboard=True,
)
