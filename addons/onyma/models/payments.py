# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *


class OnymaPayments(models.Model):
    _name = 'onyma.payments'

    name = fields.Char()

    def init_connection(self, rec, auth_params):
        conn = connection()
        conn_str = conn.get_odoo_connection({
            'engine': rec.engine.encode('utf-8'),
            'host': rec.host.encode('utf-8'),
            'port': rec.port,
            'database': rec.database.encode('utf-8'),
            'username': rec.username.encode('utf-8'),
            'password': rec.password.encode('utf-8'),
        })
        conn.create_odoo_engine(conn_str, self.engine.encode('utf-8'), self.encoding.encode('utf-8'))
        auth_sql = self.auth_sql % (auth_params['login'], auth_params['password'],)
        conn.auth(auth_sql)
        return conn

    @api.one
    @api.depends('caption')
    def check_connect(self):
        auth_params = {
            'login': self.oper_name.encode('utf-8'),
            'password': self.oper_pass.encode('utf-8'),
        }
        conn = self.init_connection(self, auth_params)
        test_sql = '''
            select operid from api_operators where login = '%s'
        '''

        result = conn.exec_sql(test_sql % (auth_params['login'], ))
        self.caption = str(get_db_data(result))
        #conn.close()
