import aiosqlite
import datetime
from bot.config import api_id, api_hash, username
from telethon.sync import TelegramClient
from telethon import types
from datetime import datetime
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import asyncio


# async def create_db(chat):
#     async with aiosqlite.connect("user_online.db") as db:
#         await db.execute(f"""CREATE TABLE IF NOT EXISTS {chat} (
#                         день text NOT NULL,
#                         время text NOT NULL,
#                         пользователей онлайн int NOT NULL,
#                         количество пользователей int NOT NULL,
#                         количество пидорасов с невидимкой int NOT NULL
#                         );
#                    """)
#         await db.commit()
#
#
# async def async_fill_db(chat):
#     while True:
#         day = datetime.date.today()
#         time = datetime.datetime.now()
#         user_online, count_user, pidr = await dump_all_participants("@" + chat)
#         await insert_values_db(chat=chat, args=(day, time, user_online, count_user, pidr))
#         yield asyncio.sleep(10)
#
#
# async def insert_values_db(chat, args):
#     async with aiosqlite.connect("user_online.db") as db:
#         sqlite_insert = f"""INSERT INTO {chat} VALUES (?, ?, ?, ?, ?);"""
#         await db.execute(sqlite_insert, args)
#         await db.commit()
#
#
# async def read_values_db(chat):
#     async with aiosqlite.connect('user_online.db') as db:
#         cursor = await db.execute(f'SELECT * FROM {chat}')
#         rows = await cursor.fetchall()
#         await cursor.close()
#     return rows
client = TelegramClient(username, api_id, api_hash)
client.start()


async def dump_all_participants(channel):
    offset_user, users_recently, users_online = 0, 0, 0
    limit_user = 100
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
        elif type(user.status) == types.UserStatusOffline:
            if type(user.status) == types.UserStatusOffline:
                if datetime.now().timestamp() - user.status.was_online.timestamp() <= 3600:
                    users_online += 1
    users_offline = len(all_participants) - users_online - users_recently
    print(f"пользователей онлайн: {users_online}")
    print(f"пользователей, которые \"были недавно\": {users_recently}")
    print(f"пользователей не в сети: {users_offline}")
    return users_online, len(all_participants), users_recently

