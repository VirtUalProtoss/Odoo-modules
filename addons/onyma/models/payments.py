# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *


class OnymaPayments(models.Model):
    _name = 'onyma.payments'

    name = fields.Char()

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
