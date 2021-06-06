import requests
import datetime
import json


async def make_wild_request(API_TOKEN: str, last_wb_upd):
    last_wb_upd = last_wb_upd.isoformat('T')
    head = {
        'Authorization': API_TOKEN,
    }
    response = requests.get('https://suppliers-api.wildberries.ru/api/v2/orders?date_start='+ str(last_wb_upd) +'&take=10&skip=0&id=123456', headers=head)
    return response.json()