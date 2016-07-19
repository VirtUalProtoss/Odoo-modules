# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *


class OnymaServers(models.Model):
    _name = 'onyma.servers'

    name = fields.Char()
    caption = fields.Text()
    engine = fields.Char()
    host = fields.Char()
    port = fields.Integer()
    database = fields.Char()
    encoding = fields.Char()
    username = fields.Char()
    password = fields.Char()
    auth_sql = fields.Char()

    oper_name = fields.Char()
    oper_pass = fields.Char()


    @api.one
    @api.depends('caption')
    def check_connect(self):
        auth_params = {
            'login': self.oper_name.encode('utf-8'),
            'password': self.oper_pass.encode('utf-8'),
        }
        conn = connection(self, auth_params)
        test_sql = '''
            select operid from api_operators where login = '%s'
        '''

        result = conn.exec_sql(test_sql % (auth_params['login'], ))
        self.caption = str(get_db_data(result))
