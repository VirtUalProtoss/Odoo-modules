# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *



class OnymaOperators(models.Model):
    _name = 'onyma.operators'

    name = fields.Char()
    login = fields.Char()
    password = fields.Char()
    operid = fields.Integer()
    gid = fields.Integer()
    email = fields.Char()

    @api.one
    def get_onyma_operators(self):
        rec = self.env['onyma.servers'].search([('name', '=', 'ЦБ ТТК')])
        auth_params = {
            'login': 's.sobolevskiy',
            'password': 'NjgZYX3J',
        }
        conn = connection(self, rec, auth_params)
        obj = Onyma(conn.get_session())
        #operators = obj.get_operator_by_login(auth_params['login'])
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
        #conn.close()
