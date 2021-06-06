from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import datetime
from keyboards.default import main_menu

from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await db.create_users_table()
    user = await db.select_user(id=message.from_user.id)
    if user:
        await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=main_menu)
    else:
        await db.add_user(message.chat.id, message.from_user.full_name, datetime.datetime.now(), datetime.datetime.now())
        await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=main_menu)
