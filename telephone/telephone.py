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