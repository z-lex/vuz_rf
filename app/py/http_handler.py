from aiohttp import web
import json
from datetime import datetime
import aiohttp
#from bs4 import BeautifulSoup


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            if isinstance(o, datetime):
                return o.isoformat()
                #return str(o)
            #if isinstance(o, datetime):

        except Exception as e:
            print('cant serialize ', o, ' e=', e)
            return json.JSONEncoder.default(self, o)

class HttpHandler:

    def __init__(self, async_db=None):
        self.app = web.Application()
        self.app.add_routes([
            web.get('/', self.vuz_test),
            web.get('/vuzapi/register', self.vuz_register),
            web.get('/vuzapi/vuzlist', self.vuz_load_list),
            web.get('/vuzapi/{code}/profile', self.vuz_load_profile),
            web.post('/vuzapi/{name}/update_profile', self.vuz_update_profile)])
        self.async_db = async_db

    async def start_server(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, port=8080)
        await self.site.start()

    async def stop_server(self):
        self.runner.cleanup()

    async def vuz_test(self, request):
        return web.Response(text="main")

    async def vuz_register(self, request):
        return web.Response(text="registered")

    async def vuz_auth(self, request):
        return web.Response(text="auth")

    async def vuz_load_list(self, request):
        if self.async_db is None:
            return web.Response(text="no db connection")
        try:
            vuz_list = await self.async_db.get_university_list()
            vuz_list['Status'] = 'ok'
            return web.json_response(json.dumps(vuz_list, indent=4, cls=CustomJSONEncoder))
        except Exception as e:
            return web.json_response(json.dumps({'Status':'err', 'info': str(e)}))

    async def vuz_load_profile(self, request):
        if self.async_db is None:
            return web.Response(text="no db connection")
        try:
            vuz_code = request.match_info.get('code', 'none')
            vuz_profile = await self.async_db.get_university_profile(univ_code=vuz_code)
            return web.json_response(json.dumps(vuz_profile, indent=4, cls=CustomJSONEncoder))
        except Exception as e:
            return web.json_response(json.dumps({'Status':'err','info': str(e)}))


    async def vuz_update_profile(self, request):
        return web.Response(text="profile updated")



if __name__ == '__main__':
    handler = HttpHandler()
    web.run_app(handler.app)
