from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .choice_states import close

count_record = InlineKeyboardMarkup(row_width=2)

all_record = InlineKeyboardButton(text='Все посты', callback_data='all')
count_record.insert(all_record)
count_record.insert(close)
