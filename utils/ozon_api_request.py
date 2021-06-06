import datetime

import requests
import json


async def do_ozon_api_request(API_KEY: str, CLIENT_ID: str, last_ozon_upd):

    '''Для работы с АПИ Озона нам нужно отформатировать дейттайм из нашей БД в нужный формат строки для отправки на серв,
    что бы там не возникало ошибок при обработке запроса, за это отвечают две след. строки'''
    last_ozon_upd = str(last_ozon_upd)
    formated_last_upd = last_ozon_upd[:10] + 'T' + last_ozon_upd[11:23] + 'Z'

    url = "https://api-seller.ozon.ru"  # Cсылку нужно поменять на боевую среду
    method = "/v2/posting/fbs/list"  # Сюда вбиваем нужный метод
    head = {
        "Client-Id": CLIENT_ID,  # сюда клиент id
        "Api-Key": API_KEY  # Сюда Api-Key
    }

    # Сюда пишем параметры запроса
    body = {
        "dir": "asc",
        "filter": {
            "since": formated_last_upd,
            "status": "awaiting_packaging",
        },
        "limit": 1,
        "offset": 0,
        "with": {
          "barcodes": True
        }
    }
    body = json.dumps(body)  # Нужно передавать в озон именно так, потому что string он как json не понимает
    response = requests.post(url + method, headers=head, data=body)

    resp = response.json()
    return resp
