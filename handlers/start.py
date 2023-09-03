import random
import re

from aiogram.utils.deep_linking import _create_link

from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import Database
from const import START_MENU_TEXT
from keyboards.start_keyboard import (
    # start_kb,
    admin_select_user_keyboard, new_start_kb, like_dislike_profiles_keyboard
)
async def start_button(message: types.Message):
    print(message)
    token = message.get_full_command()
    if token[1]:
        print(token[1])
        link = await _create_link(link_type="start", payload=token[1])
        owner = Database().select_owner_link_command(link=link)
        print(owner)
        Database().sql_insert_reference_users_command(
            owner_telegram_id=owner[0]['telegram-id'],
            reference_telegram_id=message.from_user.id
        )
    await Database().sql_insert_users(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )
    # with open("/Users/adiletsaparbek/PycharmProjects/geek_32_1/media/images.png", "rb") as photo:
    #     await bot.send_photo(
    #         chat_id=message.chat.id,
    #         photo=photo,
    #         caption=START_MENU_TEXT,
    #         reply_markup=await start_kb()
    #     )
    with open("/Users/adiletsaparbek/PycharmProjects/geek_32_1/media/dostbot_animation.gif",
              "rb") as animation:
        await bot.send_animation(
            chat_id=message.chat.id,
            animation=animation,
            caption=START_MENU_TEXT.format(
                user=message.from_user.username
            ),
            reply_markup=await new_start_kb(),
            parse_mode=types.ParseMode.MARKDOWN

        )


async def secret_word(message: types.Message):
    if message.from_user.id == 1150258083:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Welcome home master {message.from_user.username}",
            reply_markup=await admin_select_user_keyboard()
        )


async def random_profiles(call: types.CallbackQuery):
    forms = Database().sql_select_user_forms()
    random_form = random.choice(forms)
    print(random_form)
    with open(random_form["photo"], "rb") as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=f"*Nickname:* {random_form['nickname']}\n"
                    f"*Age:* {random_form['age']}\n"
                    f"*Bio:* {random_form['bio']}\n",
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=await like_dislike_profiles_keyboard(
                form_telegram_id=random_form['telegram_id']
            )
        )


async def like_call(call: types.CallbackQuery):
    print("someone liked form")
    print(f"like_call {call}")
    owner_telegram_id = re.sub("like_", "", call.data)
    liked_form = Database().sql_liked_form_command(
        owner_telegram_id=owner_telegram_id,
        liker_telegram_id=call.from_user.id
    )
    print(liked_form)
    if liked_form:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='You already liked this form'
        )
        await random_profiles(call=call)
    else:
        Database().sql_insert_like_form_command(
            owner_telegram_id=owner_telegram_id,
            liker_telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=owner_telegram_id,
            text="Someone liked your form 🤟🏻"
        )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=["start"])
    dp.register_message_handler(secret_word, lambda word: "dorei" in word.text)
    dp.register_callback_query_handler(random_profiles, lambda call: call.data == "random_profiles")
    dp.register_callback_query_handler(like_call, lambda call: "like_" in call.data)