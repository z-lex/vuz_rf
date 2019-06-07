import socket
import asyncio
import struct
import json
import os

class ExchangeSocket:
    def __init__(self, addr="/tmp/test.sock", async_db=None):
        os.system('rm -f {0}'.format(addr))
        self.addr = addr
        self.async_db = async_db
        self.sock_server = None
        self.reader = None
        self.writer = None

    async def start_server(self):
        print('in start server')
        self.sock_server = await asyncio.start_unix_server(self.on_client_connected,
                                                           path=self.addr)
        async with self.sock_server:
            await self.sock_server.serve_forever()

    async def on_client_connected(self, reader, writer):
        print('in client connected')
        self.reader = reader
        self.writer = writer
        while True:
            try:
                req_raw = await reader.readline()
                req = json.loads(req_raw.decode())
                await self.process_request(req)
                return # для каждого запроса - подключение
            except Exception as e:
                print("message loop (on_client_connected): ", e)
                return

    async def process_request(self, req):
        print('request: ', req)
