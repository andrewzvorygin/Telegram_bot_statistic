import sys
from time import sleep
# pip install telethon==0.11.5
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.types import ChannelParticipantsSearch, InputChannel
from bot.config import api_id, api_hash

limit = 100



async def test():
    channel_id = 'https://t.me/urfu_ru'
    client = TelegramClient('current-session', api_id, api_hash)

    client = client.start()
    x = client.get_participants(channel_id)
    print(x)


async def main():
    await test()

asyncio.run(main())
# def get_online():
#
#     client.connect()
#     dump_users(get_chat_info(channel_id, client), client)
#
#
# def get_chat_info(username, client):
#     chat = client(ResolveUsernameRequest(username))
#     result = {
#         'chat_id': chat.peer.channel_id,
#         'access_hash': chat.chats[0].access_hash
#     }
#     return result
#
#
# def dump_users(chat, client):
#     counter = 0
#     offset = 0
#     # нам нужно сделать объект чата, как сказано в документации
#     chat_object = InputChannel(chat['chat_id'], chat['access_hash'])
#     all_participants = []
#     while True:
#         # тут мы получаем пользователей
#         # всех сразу мы получить не можем для этого нам и нужен offset
#         participants = client.invoke(GetParticipantsRequest(
#                     chat_object, ChannelParticipantsSearch(''), offset, limit
#                 ))
#         print(participants.users)
#         # если пользователей не осталось, т.е мы собрали всех, выходим
#         if not participants.users:
#             break
#         all_participants.extend(['{} {}'.format(x.id, x.username) for x in participants.users])
#         users_count = len(participants.users)
#         # увеличиваем offset на то кол-во юзеров которое мы собрали
#         offset += users_count
#         counter += users_count
#         print('{} users collected'.format(counter))
#         # не забываем делать задержку во избежания блокировки
#         sleep(2)
#     # сохраняем в файл
#     with open('users.txt', 'w') as file:
#         file.write('\n'.join(map(str, all_participants)))
#

