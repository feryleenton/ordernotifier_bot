from aiogram import executor
import asyncio
import json
from utils.ozon_api_request import do_ozon_api_request
from utils.wild_api_request import make_wild_request

from aiogram.utils.exceptions import ChatNotFound

from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        users = await db.select_all_users()

        for user in users:
            try:
                # make API request here
                if user[2] and user[6]:
                    print(user)
                    # if Ozon API key and client id exists
                    result = await do_ozon_api_request(user[2], user[6], user[4])
                    print(result)
                    for order in result['result']:
                        msg = '<b>У вас новый заказ на Ozon !</b> \n' \
                              'Заказ оформлен: ' + str(order['created_at']) + '\n\n'
                        for product in order['products']:
                            msg += str(product['name']) + '\n' \
                                'Количество: ' + str(product['quantity']) + '\n' \
                                'По цене: ' + str(product['price']) + '\n\n'
                        await bot.send_message(user[0], msg, parse_mode='html')
                    await db.update_ozon_last_upd(user[0])
                if user[3]:
                    # if wb API key exists
                    result = await make_wild_request(user[3], user[5])
                    await bot.send_message(user[0], result)
                    print(result)
            except ChatNotFound:
                # deleting user from DB if chat not found, made for optimization
                await db.delete_user(user[0])


if __name__ == '__main__':
    dp.loop.create_task(scheduled(10))
    executor.start_polling(dp, on_startup=on_startup)
