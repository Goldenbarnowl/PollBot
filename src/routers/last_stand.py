import asyncio

from aiogram import Router, F
from aiogram.types import Message

from config import bot, admin_group
from phrases import LAST_STAND

last_stand_router = Router()


@last_stand_router.message()#F.chat.id != admin_group)
async def handle_last_stand(message: Message):
    chat_id = message.chat.id
    await bot.send_message(
        chat_id=chat_id,
        text=LAST_STAND
    )
    print(message)
