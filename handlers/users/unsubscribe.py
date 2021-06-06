from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import main_menu

from loader import dp, db


@dp.message_handler(text='Отписаться')
async def unsubscribe_user(message: types.Message):
    user = await db.select_user(id=message.from_user.id)
    await db.delete_user(message.from_user.id)
    await message.answer('Вы отписались от уведомлений !', reply_markup=ReplyKeyboardRemove())