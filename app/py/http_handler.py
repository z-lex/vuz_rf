from aiohttp import web
import json
import base64
from datetime import datetime
import aiohttp
from docs_recognition import Recognizer

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
            web.get('/universities', self.vuz_load_list),
            web.get('/universities/{code}/info', self.vuz_load_profile),
            web.put('/universities/{code}', self.vuz_update_profile),
            web.get('/universities/info', self.vuz_load_all_profiles),
            web.post('/universities/recognize', self.recognize_docs),
            web.post('/universities/{code}/docs', self.vuz_post_docs),
        ])
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

    async def vuz_load_all_profiles(self, request):
        try:
            vuz_list = await self.async_db.get_university_list()
            res_dict = dict()
            for vuz_code in vuz_list.keys():
                vuz_profile = await self.async_db.get_university_profile(univ_code=vuz_code)
                res_dict[vuz_code] = vuz_profile

            return web.json_response(json.dumps(res_dict, indent=4, cls=CustomJSONEncoder))

        except Exception as e:
            return web.json_response(json.dumps({'Status':'err', 'info': str(e)}))

    async def vuz_update_profile(self, request):
        return web.Response(text="profile updated")

    async def recognize_docs(self, request):
        data = await request.json()
        resp = dict()
        try:
            for doc in data['Docs']:
                if 'jpeg' in doc['ContentType']:
                    ext = 'jpeg'
                elif 'png' in doc['ContentType']:
                    ext = 'png'
                else: continue
                recog = Recognizer()
                bin_data = base64.b64decode(doc['Data'])

                if doc['Type'] =='snils':
                    filename = 'snils.'+ext
                    ff = open(filename, 'wb')
                    ff.write(bin_data)
                    ff.close()
                    resp[doc['ID']] = recog.recognize_SNILS_file(filename)
                elif doc['Type'] == 'oms':
                    filename = 'oms.'+ext
                    ff = open(filename, 'wb')
                    ff.write(bin_data)
                    ff.close()
                    resp[doc['ID']] = recog.recognize_OMS_file(filename)
                else:
                    continue
            return web.json_response(json.dumps(resp))
        except Exception as e:
            print('cant recognize: ', e)


    async def vuz_post_docs(self, request):

        reader = await request.multidict()

        field = await reader.next()
        assert field.name == 'UserID'

        type = await field.read(decode=True)
        type = type.decode('utf-8')

        field = await reader.next()
        #assert field.name == 'data'

        recog = Recognizer()

        filename = field.filename

        size = 0
        with open(filename, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)

        # распознавание поступивших документов
        data = {}
        if str(type) =='snils':
            data = recog.recognize_SNILS_file(filename)
        elif str(type) == 'oms':
            data = recog.recognize_OMS_file(filename)
        print(data)
        payload = json.dumps(data)
        return web.json_response(payload)



if __name__ == '__main__':
    handler = HttpHandler()
    web.run_app(handler.app, port=8181)
