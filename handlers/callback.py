import re

from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import Database
from keyboards.start_keyboard import quiz_1_keyboard, quiz_2_keyboard, my_profile_detail_keyboard, my_profile_create_form_keyboard, save_news_keyboard

from scraping.news_scraper import NewsScraper
async def quiz_1(message: types.Message):
    question = "Who invented Python"
    options = [
        "Voldemort",
        "Harry Potter",
        "Linus Torvalds",
        "Guido Van Rossum"
    ]

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        is_anonymous=False,
        type="quiz",
        correct_option_id=3,
        reply_markup=await quiz_1_keyboard()
    )


async def quiz_2(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Male or Female',
        reply_markup=await quiz_2_keyboard()
    )


async def answer_male(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="You are male"
    )


async def answer_female(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="You are female"
    )


async def admin_user_list_call(call: types.CallbackQuery):
    users = await Database().sql_admin_select_username_users_table()
    print(users)
    data = []
    for user in users:
        if not user["username"]:
            data.append(f'[{user["first_name"]}](tg://user?id={user["telegram_id"]})')
        else:
            data.append(f'[{user["username"]}](tg://user?id={user["telegram_id"]})')

    data = "\n".join(data)
    await call.message.reply(text=data,
                             parse_mode=types.ParseMode.MARKDOWN)


async def my_profile_call(call: types.CallbackQuery):
    user_form = Database().sql_select_user_form_by_telegram_id(
        telegram_id=call.from_user.id
    )
    try:
        with open(user_form[0]["photo"], "rb") as photo:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=f"*Nickname:* {user_form[0]['nickname']}\n"
                        f"*Age:* {user_form[0]['age']}\n"
                        f"*Bio:* {user_form[0]['bio']}\n",
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=await my_profile_detail_keyboard(
                    telegram_id=call.from_user.id
                )
            )
    except IndexError as e:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="You have no forms\n"
                 "Do you want to create one ?",
            reply_markup=await my_profile_create_form_keyboard()
        )


async def pass_creation_user_form_call(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )


async def update_form_call(call: types.CallbackQuery):
    telegram_id = re.sub("update_form_", "", call.data)
    print(f"update form print {telegram_id}")


async def delete_profile_call(call: types.CallbackQuery):
    Database().sql_delete_user_form_command(
        telegram_id=call.from_user.id
    )
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Deleted Successfully"
    )


async def news_parsing_call(call: types.CallbackQuery):
    scraper = NewsScraper()
    urls = scraper.parse_data()

    for url in urls:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=url,
            reply_markup=await save_news_keyboard(url=url)
        )


def register_callback_handlers(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=["quiz"])
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_callback_query_handler(answer_male, lambda call: call.data == "answer_male")
    dp.register_callback_query_handler(answer_female, lambda call: call.data == "answer_female")
    dp.register_callback_query_handler(admin_user_list_call, lambda call: call.data == "admin_user_list")
    dp.register_callback_query_handler(my_profile_call, lambda call: call.data == "my_profile")
    dp.register_callback_query_handler(update_form_call, lambda call: "update_form_" in call.data)
    dp.register_callback_query_handler(delete_profile_call, lambda call: call.data == "delete_form")
    dp.register_callback_query_handler(pass_creation_user_form_call, lambda call: call.data == "pass_creation")
    dp.register_callback_query_handler(news_parsing_call, lambda call: call.data == "news_parsing")