from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
import logging
import json
import os

from model import BotUsers, pg_db


load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher(bot)


async def start_broadcast(data: str):
    """Send message with new price to all users"""
    product = json.loads(data)
    _users = [user for user in BotUsers.select()]

    for user in _users:
        msg = f"{product['title']} - {product['price']}€\n"
        await bot.send_message(user, msg)


@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    """Send welcome message"""
    BotUsers.get_or_create(id=message.from_user.id, name=message.from_user.full_name)
    await message.reply("Hi!\nBot will send prices updates.\n")


async def start_bot():
    pg_db.create_tables([BotUsers])
    await dp.start_polling()


async def main():
    task = asyncio.create_task(start_bot())
    await task


if __name__ == '__main__':
    asyncio.run(main())
