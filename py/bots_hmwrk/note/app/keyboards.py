from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='INFO')],
    [KeyboardButton(text='Add task')],
    [KeyboardButton(text='SHOW')]
],
resize_keyboard=True,
one_time_keyboard = True
)

allTaskKb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='task')]])
