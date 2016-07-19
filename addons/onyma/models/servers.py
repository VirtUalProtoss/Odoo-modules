# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *
from ..billing.onyma import Onyma


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
    def get_auth_params(self):
        return {
            'login': self.oper_name.encode('utf-8'),
            'password': self.oper_pass.encode('utf-8'),
        }

    @api.one
    @api.depends('caption')
    def check_connect(self):
        auth_params = self.get_auth_params()[0]
        conn = connection(self, auth_params)
        test_sql = '''
            select operid from api_operators where login = '%s'
        '''

        result = conn.exec_sql(test_sql % (auth_params['login'], ))
        self.caption = str(get_db_data(result))

    @api.one
    def get_onyma_operators(self):
        #rec = self.env['onyma.servers'].search([('name', '=', 'ЦБ ТТК')])[1]
        #print rec
        auth_params = self.get_auth_params()[0]
        conn = connection(self, auth_params)

        obj = Onyma(conn.get_session())
        operators = obj.get_operators_by_gid(24193)
        for oper in operators:
            odoo_oper = self.env['onyma.operators'].search([('operid', '=', oper.operid)])
            if not odoo_oper.id:
                self.env['onyma.operators'].create({
                    'operid': oper.operid,
                    'name': oper.name,
                    'login': oper.login,
                    'gid': oper.gid,
                    'email': oper.email
                })
