from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

close = InlineKeyboardButton(text='Закрыть', callback_data='close')

choice = InlineKeyboardMarkup(row_width=2)
yes = InlineKeyboardButton(text='Да', callback_data='yes')
choice.insert(yes)
no = InlineKeyboardButton(text='Нет', callback_data='no')
choice.insert(no)
choice.insert(close)


state_stat = InlineKeyboardMarkup(row_width=2)
count_user = InlineKeyboardButton(text='Количество пользователей', callback_data='count_user')
state_stat.insert(count_user)
number_views_record = InlineKeyboardButton(text='Число просмотров постов', callback_data='number_views_record')
state_stat.insert(number_views_record)
state_stat.insert(close)