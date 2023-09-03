from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from config import bot
from aiogram import types, Dispatcher
from database.sql_commands import Database
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.fsm_form_keyboard import my_profile_keyboard


class FormStates(StatesGroup):
    nickname = State()
    age = State()
    bio = State()
    photo = State()


async def fsm_start(call: types.CallbackQuery):
    await call.message.reply("Send me your Nickname, please")
    await FormStates.nickname.set()


async def load_nickname(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data["nickname"] = message.text

    await FormStates.next()
    await message.reply("Send me your age, use only numeric text")


async def load_age(message: types.Message,
                   state: FSMContext):
    if type(int(message.text)) != int:
        await message.reply("Use only numeric text, please restart signup process")
        await state.finish()
    else:
        async with state.proxy() as data:
            data["age"] = message.text
        await FormStates.next()
        await message.reply(
            "Send me your bio or hobby"
        )


async def load_bio(message: types.Message,
                   state: FSMContext):
    async with state.proxy() as data:
        data["bio"] = message.text
    await FormStates.next()
    await message.reply("Send me your photo, please")


async def load_photo(message: types.Message,
                     state: FSMContext):
    path = await message.photo[-1].download(
        destination_dir="/Users/adiletsaparbek/PycharmProjects/geek_32_1/media"
    )

    async with state.proxy() as data:
        existed_form = Database().sql_select_user_form_by_telegram_id(
            telegram_id=message.from_user.id
        )
        print(existed_form)
        if existed_form:
            updated_form = Database().update_user_form_command(
                telegram_id=message.from_user.id,
                nickname=data['nickname'],
                age=data['age'],
                bio=data['bio'],
                photo=path.name,
            )
            print("***updated_form: ", updated_form)
            await state.finish()
        else:
            Database().sql_insert_user_form(
                telegram_id=message.from_user.id,
                nickname=data['nickname'],
                age=data['age'],
                bio=data['bio'],
                photo=path.name,
            )
            await state.finish()
            await message.reply("Congrats, Registered Successfully",
                                reply_markup=await my_profile_keyboard())


def register_fsm_form_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(fsm_start, lambda call: call.data == "signup")
    dp.register_message_handler(load_nickname, content_types=["text"],
                                state=FormStates.nickname)
    dp.register_message_handler(load_age, content_types=["text"],
                                state=FormStates.age)
    dp.register_message_handler(load_bio, content_types=['text'],
                                state=FormStates.bio)
    dp.register_message_handler(load_photo, content_types=ContentType.PHOTO,
                                state=FormStates.photo)