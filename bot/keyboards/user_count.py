from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .choice_states import close

count_day = InlineKeyboardMarkup(row_width=2)

day_7 = InlineKeyboardButton(text='7 дней', callback_data='7 day')
count_day.insert(day_7)
day_10 = InlineKeyboardButton(text='14 дней', callback_data='10 day')
count_day.insert(day_10)
month_1 = InlineKeyboardButton(text='1 месяц', callback_data='1 month')
count_day.insert(month_1)
month_3 = InlineKeyboardButton(text='3 месяца', callback_data='3 month')
count_day.insert(month_3)
month_6 = InlineKeyboardButton(text='6 месяцев', callback_data='6 month')
count_day.insert(month_6)
count_day.insert(close)