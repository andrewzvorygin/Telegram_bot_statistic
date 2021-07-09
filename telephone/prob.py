from telethon.sync import TelegramClient
from telethon import types
import matplotlib.pyplot as plt
from bot.config import api_id, api_hash, username

api_id = api_id
api_hash = api_hash
username = username


async def get_graph_path(chat, limit=0, min_id=0, max_id=0):
    count_views, record_id = [], []
    async with TelegramClient(username, api_id, api_hash) as client:
        async for message in client.iter_messages(chat, limit=limit, min_id=min_id, max_id=max_id):
            if type(message) == types.MessageService:
                continue
            count_views.append(message.views)
            record_id.append(message.id)
    path = draw_graph(count_views, record_id)
    return path


def draw_graph(count_views, record_id):
    name = id(record_id)
    path = f'telephone\\{name}.jpg'
    plt.plot(record_id, count_views)
    plt.title('Статистика просмотров постов', fontsize=15, )
    plt.xlabel('ID поста', fontsize=12, color='blue')
    plt.ylabel('Количество просмотров', fontsize=12, color='blue')
    plt.grid(True)
    plt.savefig(path)
    return path


get_graph_path('https://t.me/urfu_ru', limit=50)
