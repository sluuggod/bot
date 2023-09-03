import re

from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import Database
from keyboards.reference_keyboard import reference_menu_keyboard
from keyboards.start_keyboard import (
    quiz_1_keyboard,
    quiz_2_keyboard,
    my_profile_detail_keyboard,
    my_profile_create_form_keyboard,
)
from aiogram.utils.deep_linking import _create_link
import binascii
import os
from const import REFERENCE_MENU_TEXT, CREATION_REFERENCE_LINK_TEXT


async def reference_menu_call(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=REFERENCE_MENU_TEXT,
        reply_markup=await reference_menu_keyboard(),
        parse_mode=types.ParseMode.MARKDOWN
    )


async def create_reference_link(call: types.CallbackQuery):
    is_link_exist = Database().select_existed_link(
        telegram_id=call.from_user.id
    )
    if is_link_exist[0]['link'] is None:
        token = binascii.hexlify(os.urandom(4)).decode()
        link = await _create_link(link_type="start", payload=token)
        Database().update_user_by_reference_link_command(
            link=link,
            telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=CREATION_REFERENCE_LINK_TEXT.format(
                link=link,
            ),
            parse_mode=types.ParseMode.MARKDOWN_V2
        )
    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text=CREATION_REFERENCE_LINK_TEXT.format(
                link=is_link_exist[0]['link'],
            ),
            parse_mode=types.ParseMode.MARKDOWN_V2)


def register_reference_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(reference_menu_call,
                                       lambda call: call.data == "reference_menu")
    dp.register_callback_query_handler(
        create_reference_link,
        lambda call: call.data == "reference_link_creation"
    )