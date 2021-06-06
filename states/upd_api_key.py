from aiogram.dispatcher.filters.state import StatesGroup, State


class UPD_API_Key(StatesGroup):
    WAITING_FOR_OZON_API_KEY = State()
    WAITING_FOR_CLIENT_ID = State()
    WAITING_FOR_WID_API_KEY = State()