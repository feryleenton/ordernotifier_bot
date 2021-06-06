import asyncio
import datetime

import asyncpg as asyncpg

from data import config


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.PGUSER,
                password=config.PGPASSWORD,
                host=config.IP,
            )
        )

    async def create_users_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        ozon_api_key VARCHAR(255),
        wildberries_api_key VARCHAR(255),
        last_ozon_upd TIMESTAMP,
        last_wb_upd TIMESTAMP,
        ozon_client_id VARCHAR(255),
        PRIMARY KEY (id)
        )
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, id: int, name: str, last_upd=None, last_wb_upd=None):
        sql = "INSERT INTO Users (id, name, last_ozon_upd, last_wb_upd) VALUES ($1, $2, $3, $4)"

        await self.pool.execute(sql, id, name, last_upd, last_wb_upd)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.pool.fetch(sql)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def update_ozon_api_key(self, ozon_api_key, id):
        sql = "UPDATE Users SET ozon_api_key = $1 WHERE id = $2"
        return await self.pool.execute(sql, ozon_api_key, id)

    async def update_ozon_client_id(self, ozon_client_id, id):
        sql = "UPDATE Users SET ozon_client_id = $1 WHERE id = $2"
        return await self.pool.execute(sql, ozon_client_id, id)

    async def delete_user(self, id: int):
        sql = 'DELETE FROM Users WHERE id = $1'
        return await self.pool.execute(sql, id)

    async def update_wildberries_api_key(self, wildberries_api_key, id):
        sql = "UPDATE Users SET wildberries_api_key = $1 WHERE id = $2"
        return await self.pool.execute(sql, wildberries_api_key, id)

    async def update_ozon_last_upd(self, id):
        sql = "UPDATE Users SET last_ozon_upd = $1 WHERE id = $2"
        return await self.pool.execute(sql, datetime.datetime.now(), id)

    async def update_wb_last_upd(self, id):
        sql = "UPDATE Users SET last_wb_upd = $1 WHERE id = $2"
        return await self.pool.execute(sql, datetime.datetime.now(), id)


db = Database(loop=asyncio.get_event_loop())