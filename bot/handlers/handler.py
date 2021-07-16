from bot.loader import dp, bot
from aiogram.types import Message, CallbackQuery
from bot.keyboards.choice_states import choice, state_stat
from bot.keyboards.user_count import count_day
from bot.keyboards.record_count import count_record, interval_record, close_all
from bot.states import Statistic
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import logging
from telephone.prob import get_graph_path
from os import remove
from telephone import telephone


@dp.message_handler(commands=["start"])
async def start_bot(message: Message, state: FSMContext):
    await message.answer('Отправьте ссылку на канал, о котором хочешь получить информацию, '
                         'без лишних символов и пробелов')
    await Statistic.ChoiceChannel.set()
    logging.info('Переход в состояние выбора канала')


@dp.message_handler(state=Statistic.ChoiceChannel)
async def get_channel(message: Message, state: FSMContext):
    url = message.text
    if len(url.split('/')) > 1:
        short_url = '@' + url.split('/')[-1]
    else:
        short_url = url
    await state.update_data(url=short_url[1:])
    logging.info(f'Получили ссылку на канал url : {url} \n short_url : {short_url}')
    await message.answer(f'Вы запросили информацию о канале {short_url}', reply_markup=choice)
    logging.info('Запросили подтверждение сбора статистики о канале')


@dp.callback_query_handler(text_contains="no", state=Statistic.ChoiceChannel)
async def false_channel(call: CallbackQuery):
    logging.info('Неверный канал, выбор нового канала')
    await call.answer(cache_time=60)
    await call.message.answer('Выберите другой канал для анализа')


@dp.callback_query_handler(text_contains="yes", state=Statistic.ChoiceChannel)
async def true_channel(call: CallbackQuery, state: FSMContext):
    logging.info('Верный канал, выбор действия')
    await call.answer(cache_time=60)
    data = await state.get_data()
    chat = data['url']
    await telephone.create_db(chat)
    await call.message.answer('Статистику чего вы хотите изучить?', reply_markup=state_stat)
    telephone.async_fill_db(chat)


@dp.callback_query_handler(text_contains="count_user", state=Statistic.ChoiceChannel)
async def choice_count_day(call: CallbackQuery, state: FSMContext):
    logging.info('Выборали статистику количества пользователей')
    logging.info('Выбирают количество дней')
    await call.answer(cache_time=60)
    await Statistic.UserCountChange.set()
    await call.message.answer('За какое количество дней вы хотите получить статистику о пользователях?\n'
                              'Выбери из предложенного или введи своё значение', reply_markup=count_day)


@dp.callback_query_handler(text_contains="better_time", state=Statistic.ChoiceChannel)
async def get_better_time(call: CallbackQuery, state: FSMContext):
    logging.info('Выборали лучшее время')
    await call.answer(cache_time=60)
    await Statistic.BetterTime.set()
    data = await state.get_data()
    chat = data['url']
    rows = await telephone.read_values_db(chat)
    await call.message.answer(rows)


# После этот метод должен возвращать статистку по количеству пользователей за выбранный период
@dp.callback_query_handler(Text(equals=['7 day', '10 day', '1 month', '3 month', '6 month']),
                           state=Statistic.UserCountChange)
async def get_user_statistic(call: CallbackQuery = None, message: Message = None):
    await call.answer(cache_time=60)
    logging.info('Выбираем количсетво дней')
    if call.data is not None:
        value = call.data
        logging.info(f'call.data : {value}')
    else:
        value = message.text
        logging.info(f'value : {value}')
    await call.message.answer(f'Вы выбрали график за {value}')
    logging.info('выбрали')


@dp.callback_query_handler(text_contains="number_views_record", state=Statistic.ChoiceChannel)
async def choice_count_record(call: CallbackQuery, state: FSMContext):
    logging.info('Выборали статистику по постам')
    await call.answer(cache_time=60)
    await Statistic.NumberViewsRecord.set()
    await call.message.answer('За какое количество постов вы хотите получить статистику?\n'
                              'Вы можете посмотреть статистику за всё время, нажав на кнопку, '
                              'либо написать количество постов за которое вы хотите узнать статистику',
                              reply_markup=count_record)


@dp.callback_query_handler(text_contains="close", state=Statistic)
async def close(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.finish()
    await call.message.answer('Закрыли')


@dp.callback_query_handler(text_contains="interval", state=Statistic.NumberViewsRecord)
async def set_interval_record(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    logging.info('Вводят интервал статистики по постам')
    await Statistic.RecordInterval.set()
    await call.message.answer('Введите интеравал id сообщений через пробел, '
                              'с какого и по какое хотите посмотреть статистику.\n'
                              '<b>Пример: </b>5 10. \nС 5 и по 10 сообщение вы увидите статистику')


@dp.callback_query_handler(state=Statistic.NumberViewsRecord)
async def get_answer_graph_limit(call: CallbackQuery = None, state: FSMContext = None):
    await call.answer(cache_time=60)
    data = await state.get_data()
    chat = data['url']
    limit = int(call.data)
    path = await get_graph_path(chat, limit=limit)
    path = 'C:\\Users\\andre\\OneDrive\\Рабочий стол\\Telegram_bot_statistic\\' + path
    with open(path, 'rb') as photo:
        await call.message.answer_photo(photo, reply_markup=interval_record)
    remove(path)


@dp.message_handler(state=Statistic.RecordInterval)
async def get_graph_id_record(message: Message, state: FSMContext = None):
    logging.info('Ввели интервал, обрабатываемЧ')
    data = await state.get_data()
    chat = data['url']
    try:
        min_id, max_id = map(int, message.text.split())
        if max_id <= min_id:
            await message.answer('Неверно указан интервал', reply_markup=close_all)
        else:
            path = await get_graph_path(chat, min_id=min_id, max_id=max_id)
            path = 'C:\\Users\\andre\\OneDrive\\Рабочий стол\\Telegram_bot_statistic\\' + path
            with open(path, 'rb') as photo:
                await message.answer_photo(photo, reply_markup=close_all)
            remove(path)
    except Exception:
        await message.answer('Неверно указан интервал', reply_markup=close_all)





@dp.message_handler()
async def exo(message: Message):
    await message.answer(f'Ты написал {message.text}.\n Я жду команду /start')
