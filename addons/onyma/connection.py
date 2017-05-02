# -*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData
from sqlalchemy.engine.result import RowProxy, ResultProxy


def get_db_data(res):
    data = []
    if res:
        row_count = 0
        for row in res:
            r_data = get_db_data_row(row)
            row_count += 1
            data.append(r_data)
    return data


def get_db_data_row(row):
    r_data = {}
    if type(row) == RowProxy:
        keys = row._keymap
        for key in keys:
            if type(key) == str or type(key) == unicode:
                r_data.update({key: row[keys[key][2]], })
    else:
        for col in row.__dict__:
            r_data.update({col: row.__dict__[col], })
    return r_data


class connection():

    __connection_template = '%(engine)s://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s'

    def __init__(self, rec, auth_params, echo=False):
        self.__verbose = echo
        conn_str = self.get_connection({
            'engine': rec.engine.encode('utf-8'),
            'host': rec.host.encode('utf-8'),
            'port': rec.port,
            'database': rec.database.encode('utf-8'),
            'username': rec.username.encode('utf-8'),
            'password': rec.password.encode('utf-8'),
        })
        self.create_engine(conn_str, rec.engine.encode('utf-8'), rec.encoding.encode('utf-8'))
        self.create_session()
        auth_sql = rec.auth_sql.encode('utf-8') % (auth_params['login'], auth_params['password'],)
        self.auth(auth_sql)

    def get_connection(self, params):
        return self.__connection_template % ({
            'engine': params['engine'],
            'username': params['username'],
            'password': params['password'],
            'host': params['host'],
            'port': str(params['port']),
            'database': params['database'],
        })

    def get_engine_type(self, engine_string):
        eng_arr = engine_string.split('+')
        if len(eng_arr) == 1:
            sub_type = ''
        else:
            sub_type = eng_arr[1]
        return { 'type': eng_arr[0], 'sub_type': sub_type, }

    def create_engine(self, connection_string, engine, encoding='utf-8'):
        self.__engine_type = self.get_engine_type(engine)
        self.__engine = create_engine(
            connection_string,
            echo=self.__verbose,
            # coerce_to_unicode=True,
            encoding=encoding,
            convert_unicode=True
        )

    def get_engine(self):

        return self.__engine

    def auth(self, auth_sql):
        self.__metadata = MetaData(bind=self.__engine)
        if auth_sql:
            self.__engine.execute(auth_sql)

    def create_session(self):

        self.__session = sessionmaker(bind=self.__engine)()

    def exec_sql(self, sql, *params):

        return self.__engine.execute(sql, *params)

    def close(self):

        self.get_session().close()

    def alive(self):

        return self.get_session().is_active()

    def get_session(self):

        return self.__session

    def get_cursor(self):
        connection = self.__engine.raw_connection()
        self._raw_cursor = connection.cursor()
        return self._raw_cursor
