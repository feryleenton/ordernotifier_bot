from aiogram import types
from aiogram.dispatcher import FSMContext

from states import UPD_API_Key
from loader import dp, db


@dp.message_handler(state=UPD_API_Key.WAITING_FOR_CLIENT_ID)
async def updating_wb_api_key(message: types.Message, state: FSMContext):
    new_client_id = message.text
    await db.update_ozon_client_id(new_client_id, message.from_user.id)
    await message.answer('Ваши данные для Ozon обновлены !')
    await state.reset_state()


@dp.message_handler(state=UPD_API_Key.WAITING_FOR_OZON_API_KEY)
async def get_my_refs(message: types.Message, state: FSMContext):
    new_api_key = message.text
    await db.update_ozon_api_key(new_api_key, message.chat.id)
    await message.answer('Введите ваш Client ID: ')
    await UPD_API_Key.WAITING_FOR_CLIENT_ID.set()


@dp.message_handler(state=UPD_API_Key.WAITING_FOR_WID_API_KEY)
async def get_my_refs(message: types.Message, state: FSMContext):
    new_api_key = message.text
    await db.update_wildberries_api_key(new_api_key, message.chat.id)
    await message.answer('Ваш ключ API обновлен !')
    await state.reset_state()


@dp.message_handler(text='Добавить \ Обновить Ozon API Key')
async def updating_ozon_api_key(message: types.Message, state: FSMContext):
    await UPD_API_Key.WAITING_FOR_OZON_API_KEY.set()
    await message.answer('Введите свой ключ API для Ozon')


@dp.message_handler(text='Добавить \ Обновить Wildberries API Key')
async def updating_wb_api_key(message: types.Message, state: FSMContext):
    await UPD_API_Key.WAITING_FOR_WID_API_KEY.set()
    await message.answer('Введите свой ключ API для Wildberries')
