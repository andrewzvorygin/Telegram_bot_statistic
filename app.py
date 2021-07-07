from bot.loader import bot
from bot.config import admin_id


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен')


if __name__ == '__main__':
    from aiogram import executor
    from bot.handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)