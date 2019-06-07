import asyncio
from aiomysql.sa import create_engine
import sqlalchemy as sa
import re

class AsyncDatabase():
    def __init__(self, loop, db_url):
        self.db_config = None
        try:
            r = re.match(r'mysql://([\S]*):([\S]*)@([\S]*)/([\S]+)\?', db_url)
            self.db_config = {
                'user': r.group(1),
                'password': r.group(2),
                'host': r.group(3),
                'port': 3306,
                'db': r.group(4),
            }
        except Exception as e:
            print('async_dn init: ', e)

        self.loop = loop
        self.engine = None
        self.conn = None
        self.engine_created = False


    async def connect(self):
        try:
            self.engine = await create_engine(**self.db_config, loop=self.loop, charset="utf8", autocommit=True)
        except Exception as e:
            print("cant create db engine: ", e)
        else:
            if self.engine is not None:
                self.engine_created = True

    async def perform_query(self, query):
        try:
            async with self.engine.acquire() as conn:
                res_proxy = await conn.execute(query)
                (r,) = await res_proxy.fetchall()
                return r.values()
        except Exception as e:
            print("cant perform query: ", e)
            return None


    async def disconnect(self):
        if self.engine:
            self.engine.close()
            await self.engine.was_closed()
