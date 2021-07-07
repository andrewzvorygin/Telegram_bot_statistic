from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice = InlineKeyboardMarkup(row_width=2)

yes = InlineKeyboardButton(text='Да', callback_data='yes')
choice.insert(yes)
no = InlineKeyboardButton(text='Нет', callback_data='no')
choice.insert(no)