import asyncio
import select
import psycopg2
import psycopg2.extensions
import os

from bot import start_broadcast
from dotenv import load_dotenv

load_dotenv()


async def listen():
    """Listen notification from base in notify_price_change chanel"""

    connection = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS")
    )

    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()
    cursor.execute("LISTEN product_price_change;")

    while True:
        if select.select([connection], [], [], 5) == ([], [], []):
            pass
        else:
            connection.poll()
            while connection.notifies:
                print('connection..pull....')
                notification = connection.notifies.pop(0)
                await start_broadcast(notification.payload)


async def main():
    task = asyncio.create_task(listen())
    await task


if __name__ == '__main__':
    asyncio.run(main())
