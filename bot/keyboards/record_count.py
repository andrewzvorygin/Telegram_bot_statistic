from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .choice_states import close

count_record = InlineKeyboardMarkup(row_width=2)

all_record = InlineKeyboardButton(text='Все посты', callback_data='1000000')
count_record.insert(all_record)
last_20 = InlineKeyboardButton(text='Последние 20', callback_data='20')
count_record.insert(last_20)
last_50 = InlineKeyboardButton(text='Последние 50', callback_data='50')
count_record.insert(last_50)
last_100 = InlineKeyboardButton(text='Последние 100', callback_data='100')
count_record.insert(last_100)
record_id = InlineKeyboardButton(text='Ввести интервал', callback_data='interval')
count_record.insert(record_id)
count_record.insert(close)

interval_record = InlineKeyboardMarkup(row_width=2)
interval_record.insert(record_id)
interval_record.insert(close)

close_all = InlineKeyboardMarkup()
close_all.insert(close)