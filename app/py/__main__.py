from exchange_socket import ExchangeSocket
from async_db import AsyncDatabase
import os
import asyncio

async def main():

    async_db = AsyncDatabase(db_url=os.environ['DATABASE_URL'],
                             loop=asyncio.get_event_loop())
    await async_db.connect()
    sock_name = os.environ['GOLANG_SOCKET_NAME']
    ex_sock = ExchangeSocket(addr=sock_name, async_db=async_db)
    await ex_sock.start_server()

asyncio.run(main())

