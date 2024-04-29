import asyncio
import os

import select
import psycopg2
import psycopg2.extensions

import bot
from dotenv import load_dotenv

load_dotenv()


async def listen():
    """Listen notification from base in notify_price_change chanel"""

    connection = psycopg2.connect(dbname=os.environ.get("DB_NAME"),
                                  user=os.environ.get("DB_USER"),
                                  password=os.environ.get("DB_PASS"))

    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()
    cursor.execute("LISTEN notify_price_change;")

    while True:
        if select.select([connection], [], [], 5) == ([], [], []):
            pass
        else:
            connection.poll()
            while connection.notifies:
                notification = connection.notifies.pop(0)
                await bot.start_broadcast(notification.payload)


async def main():
    task = asyncio.create_task(listen())
    await task


if __name__ == '__main__':
    asyncio.run(main())