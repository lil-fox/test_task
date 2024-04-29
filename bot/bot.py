import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from db.database import User
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ.get("API_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    """Send welcome message"""
    User.get_or_create(id=message.from_user.id, name=message.from_user.full_name)
    await message.reply("Hi!\nBot will send prices updates.\n")


async def start_bot():
    await dp.start_polling()


async def main():
    task = asyncio.create_task(start_bot())
    await task


if __name__ == '__main__':
    asyncio.run(main())
