import aiosqlite
import asyncio


async def create_db(chat):
    async with aiosqlite.connect("user_online.db") as db:
        await db.execute(f"""CREATE TABLE IF NOT EXISTS {chat} (
                        date_time text NOT NULL, 
                        count_user_online int NOT NULL, 
                        count_user int NOT NULL,
                        percentage_of_users REAL NOT NULL);
                   """)
        await db.commit()


async def insert_values_db(chat, date_time, count_user_online, count_user, percentage_of_users):
    args = (date_time, count_user_online, count_user, percentage_of_users)
    async with aiosqlite.connect("user_online.db") as db:
        sqlite_insert = f"""INSERT INTO {chat} (date_time, count_user_online, count_user, percentage_of_users) VALUES (?, ?, ?, ?);"""
        await db.execute(sqlite_insert, args)
        await db.commit()


async def read_values_db(chat):
    async with aiosqlite.connect('user_online.db') as db:
        cursor = await db.execute(f'SELECT * FROM {chat}')
        rows = await cursor.fetchall()
        await cursor.close()
    return rows


async def main():
    chat = 'test'
    await create_db(chat)
    await insert_values_db(chat, '2021-07-14 18:00:00:000', 4, 10, 0.4)
    await insert_values_db(chat, '2021-07-14 19:00:00:000', 6, 10, 0.6)
    answer = await  read_values_db(chat)
    print(answer)

asyncio.run(main())


import datetime
from bot.config import api_id, api_hash, username
from telethon.sync import TelegramClient
from telethon import types
from datetime import date, datetime
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


client = TelegramClient(username, api_id, api_hash)
client.start()


async def dump_all_participants(channel):
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
