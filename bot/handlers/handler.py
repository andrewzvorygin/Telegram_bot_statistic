from bot.loader import dp
from aiogram.types import Message, CallbackQuery
from bot.keyboards.choice_states import choice, state_stat
from bot.keyboards.user_count import count_day
from bot.keyboards.record_count import count_record
from bot.states import Statistic
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import logging


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
    await state.update_data(url=short_url)
    logging.info(f'Получили ссылку на канал url : {url} \n short_url : {short_url}')
    await message.answer(f'Вы запросили информацию о канале {short_url}', reply_markup=choice)
    logging.info('Запросили подтверждение сбора статистики о канале')


@dp.callback_query_handler(text_contains="no", state=Statistic.ChoiceChannel)
async def false_channel(call: CallbackQuery):
    logging.info('Неверный канал, выбор нового канала')
    await call.answer(cache_time=60)
    # await call.message.answer('Пидора ответ')
    await call.message.answer('Выберите другой канал для анализа')


@dp.callback_query_handler(text_contains="yes", state=Statistic.ChoiceChannel)
async def true_channel(call: CallbackQuery):
    logging.info('Верный канал, выбор действия')
    await call.answer(cache_time=60)
    # await call.message.answer('Пизда')
    # await call.message.answer('Жди ответа ещё ничего не работает')
    # await call.message.answer('Ладно, отвечу, но с тебя вино этому господину @coronovirus_suka выбери,'
    #                           ' что хочешь чекнуть', reply_markup=state_stat)
    await call.message.answer('Статистику чего вы хотите изучить?', reply_markup=state_stat)


@dp.callback_query_handler(text_contains="count_user", state=Statistic.ChoiceChannel)
async def choice_count_day(call: CallbackQuery, state: FSMContext):
    logging.info('Выборали статистику количества пользователей')
    logging.info('Выбирают количество дней')
    await call.answer(cache_time=60)
    await Statistic.UserCountChange.set()
    # await call.message.answer('За какое количество дней ты хочешь статистику по пользователям?\n'
    #                           'Выбери из предложенного или введи своё значение \n'
    #                           '<b>ВВОДИТЬ ТОЛЬКО ЧИСЛО - КОЛИЧЕСТВО ДНЕЙ, НО ЭТА ХУЕТА НЕ РАБОТАЕТ, '
    #                           'ПОЭТОМУ ВЫБИРАЕМ ИЗ КНОПОК</b>', reply_markup=count_day)
    await call.message.answer('За какое количество дней вы хотите получить статистику о пользователях?\n'
                              'Выбери из предложенного или введи своё значение', reply_markup=count_day)


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


@dp.callback_query_handler(state=Statistic.NumberViewsRecord)
async def choice_count_day(call: CallbackQuery = None, message: Message = None):
    await call.answer(cache_time=60)
    if call is not None:
        answer = 'все дни'
    else:
        answer = f'{message} дней'
    await call.message.answer(f'Вы выбрали статистику за {answer}')


@dp.callback_query_handler(text_contains="close", state=Statistic)
async def choice_count_day(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.finish()
    await call.message.answer('Закрыли')


@dp.message_handler()
async def exo(message: Message):
    # await message.answer('Пиши что хочешь, мне <i><b>похуй</b></i> я жду команды /start')
    await message.answer(f'Ты написал {message.text}.\n Я жду команду /start')