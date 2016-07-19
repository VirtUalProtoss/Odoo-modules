# -*- coding: utf-8 -*-

__author__ = 'virtual'

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData


class DBConnection():

    __connection_template = '%(engine)s://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s'

    def __init__(self, server_config=None, auth_schema=None, echo=False):
        self.__verbose = echo
        if server_config and auth_schema:
            self.server_config = server_config
            self.auth_schema = auth_schema
            self.create_engine(server_config, auth_schema)
            self.create_session()
        else:
            raise AttributeError

    def get_engine_type(self, engine_string):
        eng_arr = engine_string.split('+')
        if len(eng_arr) == 1:
            sub_type = ''
        else:
            sub_type = eng_arr[1]
        return { 'type': eng_arr[0], 'sub_type': sub_type, }

    def create_engine(self, config, schema):
        connection_string = self.get_connection(config, schema)
        self.__engine_type = self.get_engine_type(config['engine'])
        self.__engine = create_engine(
            connection_string,
            echo=self.__verbose,
            #coerce_to_unicode=True,
            encoding=config['encoding'],
            convert_unicode=True
        )

    def get_engine(self):
        """
        Return DB engine.
        """
        return self.__engine

    def get_connection(self, config, schema):
        if config['engine'] == 'sqlite':
            return '%s:////%s/%s' % (
                config['engine'],
                config['path'],
                config['database'],
            )
        else:
            return self.__connection_template % ({
                'engine': config['engine'],
                'username': schema['username'],
                'password': schema['password'],
                'host': config['host'],
                'port': str(config['port']),
                'database': config['database'],
                })

    def auth_by_schema(self, schema):
        print ('Auth by schema %s' % (schema, ))
        self.__metadata = MetaData(bind=self.__engine)
        if 'auth_sql' in self.auth_schema[schema]:
            self.__engine.execute(self.auth_schema[schema]['auth_sql'])

    def auth(self, auth_sql=None):
        if not auth_sql:
            if 'auth_sql' in self.auth_schema:
                auth_sql = self.auth_schema['auth_sql']

        self.__metadata = MetaData(bind=self.__engine)
        if auth_sql:
            self.__engine.execute(auth_sql)

    def create_session(self):

        self.__session = sessionmaker(bind=self.__engine)()

    def exec_sql(self, sql, *params):

        return self.__engine.execute(sql, *params)

    def close(self):
        self.get_session().close()
        #self.get_engine().close()

    def alive(self):
        return self.get_session().is_active()

    def get_session(self):
        return self.__session

    def get_cursor(self):
        connection = self.__engine.raw_connection()
        self._raw_cursor = connection.cursor()
        return self._raw_cursor
