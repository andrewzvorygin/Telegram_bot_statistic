from bot.loader import dp
from aiogram.types import Message, CallbackQuery
from bot.keyboards.Yes_no import choice


@dp.message_handler(commands=["start"])
async def start_bot(message: Message):
    await message.answer('Отправь ссылку на канал, о котором хочешь получить информацию, без лишних символов и пробелов')


@dp.message_handler()
async def start_bot(message: Message):
    url = message.text
    short_url = '@' + url.split('/')[-1]
    await message.answer(f'Вы запросили информацию о канале {short_url}', reply_markup=choice)


@dp.callback_query_handler(text_contains="no")
async def start_game(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('ВЫберите другой канал для анализа')

