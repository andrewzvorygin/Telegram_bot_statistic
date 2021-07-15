import configparser
import json
import datetime
from bot.config import api_id, api_hash, username
from telethon.sync import TelegramClient
from telethon import types

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("config.ini")

# Присваиваем значения внутренним переменным

client = TelegramClient(username, api_id, api_hash)

client.start()


async def dump_all_participants(channel):
    """Записывает json-файл с информацией о всех участниках канала/чата"""
    offset_user = 0
    limit_user = 100
    users_online = 0
    users_recently = 0
    all_participants = []  # список всех участников канала
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel,
                                                           filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)

    for user in all_participants:
        if type(user.status) == types.UserStatusRecently:
            users_recently += 1
            continue
        if type(user.status) == types.UserStatusOffline:
            if abs(user.status.was_online.hour - datetime.now().hour + 5) >= 1 \
                    and user.status.was_online.minute <= datetime.now().minute \
                    and abs(user.status.was_online.day - datetime.now().day) > 1:
                continue
            else:
                users_online += 1
    users_offline = len(all_participants) - users_online - users_recently
    print(f"пользователей онлайн: {users_online}")
    print(f"пользователей, которые \"были недавно\": {users_recently}")
    print(f"пользователей не в сети: {users_offline}")


async def main():
    url = input("Введите ссылку на канал или чат: ")
    channel = await client.get_entity(url)
    await dump_all_participants(channel)


with client:
    client.loop.run_until_complete(main())