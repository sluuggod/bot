from datetime import timedelta

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot


async def echo_ban(message: types.Message):
    ban_words = ["damn", "fuck", 'bitch']

    if message.chat.id == -833914033:
        for word in ban_words:
            if word in message.text.lower().replace(" ", ""):
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id
                )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Сам ты такой, {message.from_user.username}!"
                )
                # await bot.ban_chat_member(
                #     chat_id=message.chat.id,
                #     user_id=message.from_user.id,
                #     until_date=datetime.now + timedelta(minutes=1)
                # )


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_ban)