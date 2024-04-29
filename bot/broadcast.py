from db.database import User
from bot import bot


async def start_broadcast(data: str):
    """Send message with new price to all users"""
    title, price = data.strip().split('-')

    users = [user for user in User.select()]

    for user in users:
        msg = f"{title} - {price}€\n"

        await bot.send_message(user.id, msg)
