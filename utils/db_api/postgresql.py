import asyncio
import asyncpg

from data import config


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool = loop.run_until_complete(
            asyncpg.create_pool(config.POSTGRES_URL
            )
        )

    @staticmethod
    def formar_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self,
                       id: int,
                       name: str,
                       language: str = 'en',
                       my_list: list = [],
                       black_list: list = []):
        sql = " INSERT INTO users " \
              "(id, name, my_list, black_list, language) " \
              "VALUES ($1, $2, $3, $4, $5)"
        await self.pool.execute(sql, id, name, my_list, black_list, language)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.pool.fetch(sql)

    async def select_user_one(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def select_users_many(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        return await self.pool.fetch(sql, *parameters)

    async def select_users_many_in_my_list(self, list_id):
        sql = "SELECT * FROM users WHERE {} = ANY(my_list)".format(list_id)
        return await self.pool.fetch(sql)

    async def update_user(self, id, update_field, update_value):
        sql = "UPDATE users SET {} = $1 WHERE id = $2".format(update_field)
        return await self.pool.execute(sql, update_value, id)

    async def delete_users(self):
        await self.pool.execute("DELETE FROM users WHERE True")


loop = asyncio.get_event_loop()
db = Database(loop)