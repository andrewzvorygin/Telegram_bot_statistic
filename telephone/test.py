import configparser
from telethon.sync import TelegramClient
import matplotlib.pyplot as plt

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import types

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']


client = TelegramClient(username, api_id, api_hash)
client.start()


class Record:
    def __init__(self, views, record_id):
        self.views = views
        self.id = record_id


# async def dump_all_messages(channel):
#     offset_msg = 0  # номер записи, с которой начинается считывание
#     limit_msg = 1000  # максимальное число записей, передаваемых за один раз
#     all_messages = []  # список всех сообщений
#     count_views = []
#     record_id = []
#     while True:
#         history = await client(GetHistoryRequest(
#             peer=channel,
#             offset_id=offset_msg,
#             offset_date=None, add_offset=0,
#             limit=limit_msg, max_id=0, min_id=0,
#             hash=0))
#         if not history.messages:
#             break
#         messages = history.messages
#         for message in messages:
#             if type(message) == types.MessageService: continue
#             all_messages.append(Record(message.views, message.id))
#             count_views.append(message.views)
#             record_id.append(message.id)
#         print(count_views)
#         print(record_id)
#         offset_msg = messages[len(messages) - 1].id
#         total_messages = len(all_messages)
#     return all_messages, count_views, record_id
async def dump_all_messages(channel):
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз
    all_messages = []  # список всех сообщений
    count_views = []
    record_id = []

    history = await client(GetHistoryRequest(
        peer=channel, offset_id=offset_msg, offset_date=None, add_offset=0,
        limit=limit_msg, max_id=0, min_id=0, hash=0))
    messages = history.messages
    for message in messages:
        if type(message) == types.MessageService: continue
        all_messages.append(Record(message.views, message.id))
        count_views.append(message.views)
        record_id.append(message.id)

    return all_messages, count_views, record_id


async def main():
    url = 'https://t.me/urfu_ru'  #input("Введите ссылку на канал или чат: ")
    channel = await client.get_entity(url)
    message_statistic, count_views, record_id = await dump_all_messages(channel)
    print(record_id)
    print(count_views)
    plt.plot(record_id, count_views)
    plt.show()


with client:
    client.loop.run_until_complete(main())
