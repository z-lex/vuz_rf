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

        # описания таблиц
        self.metadata_inc = sa.MetaData()
        self.tbl_universities = sa.Table("University", self.metadata_inc,
                                            sa.Column('idUniversity', sa.Integer, primary_key=True),
                                            sa.Column('university_name', sa.Unicode(45)),
                                            sa.Column('city', sa.Unicode(45)),
                                            sa.Column('full_address', sa.Unicode(200)),
                                            sa.Column('gps_coord1', sa.Float),
                                            sa.Column('gps_coord2', sa.Float),
                                            sa.Column('Universitycol', sa.Unicode(45)),
                                            sa.Column('website', sa.Unicode(200)))


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
                r = await res_proxy.fetchall()
                return r.values()
        except Exception as e:
            print("cant perform query: ", e)
            return str(e)

    async def get_university_list(self):
        try:
            async with self.engine.acquire() as conn:
                res_proxy = await conn.execute(
                    sa.sql.select([self.tbl_universities])
                )
                # должна быть одна запись
                (res,) = await res_proxy.fetchall()

                return dict(res.items())

        except Exception as e:
            print("get_university_list: ", e)
            return(e)

    async def get_university_profile(self, univ_code):
        profile = dict()
        try:
            async with self.engine.acquire() as conn:
                # получаем все факультеты
                res_proxy = await conn.execute('SELECT * FROM Faculty WHERE idUniversity = {0}'.format(univ_code))
                res_fac = await res_proxy.fetchall()
                profile['faculties'] = dict()
                for fac in res_fac:
                    fac_id = fac['idFaculty']
                    profile['faculties'][fac_id] = dict()
                    cont_id = fac['Con_idContacts']

                    # получаем контакты факультета

                    profile['faculties'][fac_id]['data'] = dict(fac)
                    res_proxy_cont = await conn.execute('SELECT * FROM Contacts WHERE idContacts = {0}'.format(cont_id))
                    res = await res_proxy_cont.fetchall()
                    if len(res) > 0:
                        (res,) = res

                    profile['faculties'][fac_id]['data']['phone_number'] = res['phone_number']
                    profile['faculties'][fac_id]['data']['email'] = res['email']

                    profile['faculties'][fac_id]['programmes'] = dict()
                    # для каждого факультета получаем направления
                    res_proxy_prog = await conn.execute('SELECT * FROM Programme WHERE idFaculty = {0}'.format(fac_id))
                    res_prog = await res_proxy_prog.fetchall()
                    for prog in res_prog:
                        prog_id = prog['idProgramme']
                        profile['faculties'][fac_id]['programmes'][prog_id] = dict()
                        profile['faculties'][fac_id]['programmes'][prog_id]['data'] = dict(prog)

                        profile['faculties'][fac_id]['programmes'][prog_id]['ege'] = dict()

                        # ТРЕБОВАНИЯ ЕГЭ
                        res_proxy_ege = await conn.execute("SELECT ege_dictionary.egeid, ege_dictionary.ege_name, ege_requirements.min_value FROM ege_dictionary, ege_requirements WHERE ege_dictionary.egeid = ege_requirements.egeid AND idProgramme = {0}".format(prog_id))
                        res_ege = await res_proxy_ege.fetchall()
                        for ege in res_ege:
                            profile['faculties'][fac_id]['programmes'][prog_id]['ege'][ege['egeid']] = dict()
                            profile['faculties'][fac_id]['programmes'][prog_id]['ege'][ege['egeid']]['ege_name'] = ege['ege_name']
                            profile['faculties'][fac_id]['programmes'][prog_id]['ege'][ege['egeid']]['min_value'] = ege['min_value']

                        #import pdb; pdb.set_trace()
                        # ТРЕБОВАНИЯ ВНУТРЕННИХ ЭКЗАМЕНОВ
                        profile['faculties'][fac_id]['programmes'][prog_id]['non_ege'] = dict()
                        res_proxy_non_ege = await conn.execute("SELECT non_ege_exams_dictionary.idNonEgeExam , "
                                                               "non_ege_exams_dictionary.exam_name, non_ege_exams_dictionary.max_value,"
                                                               "Programme_non_ege_ExamRequired.exam_date, Programme_non_ege_ExamRequired.min_value FROM "
                                                               "Programme_non_ege_ExamRequired, non_ege_exams_dictionary WHERE "
                                                               "Programme_non_ege_ExamRequired.idNonEgeExam = non_ege_exams_dictionary.idNonEgeExam AND idProgramme = {0}".format(prog_id))
                        res_non_ege = await res_proxy_non_ege.fetchall()
                        for non_ege in res_non_ege:
                            profile['faculties'][fac_id]['programmes'][prog_id]['non_ege'][non_ege['idNonEgeExam']] = dict()
                            profile['faculties'][fac_id]['programmes'][prog_id]['non_ege'][non_ege['idNonEgeExam']]['exam_date'] = non_ege['exam_date']
                            profile['faculties'][fac_id]['programmes'][prog_id]['non_ege'][non_ege['idNonEgeExam']]['exam_name'] = non_ege['exam_name']
                            profile['faculties'][fac_id]['programmes'][prog_id]['non_ege'][non_ege['idNonEgeExam']]['min_value'] = non_ege['min_value']
                            profile['faculties'][fac_id]['programmes'][prog_id]['non_ege'][non_ege['idNonEgeExam']]['max_value'] = non_ege['max_value']

        except Exception as e:
            print("cant perform query: ", e)
            return str(e)

        return profile

    async def disconnect(self):
        if self.engine:
            self.engine.close()
            await self.engine.was_closed()
