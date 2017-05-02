# -*- coding: utf-8 -*-

from openerp import models, fields, api


class OnymaServers(models.Model):
    _name = 'onyma.servers'

    name = fields.Char()
    caption = fields.Text()
    ext_dbsource_id = fields.Many2one('base.external.dbsource', 'External DB Source', select=True)
    auth_sql = fields.Char()

    oper_name = fields.Char()
    oper_pass = fields.Char()

    @api.one
    def get_auth_params(self):
        return {
            'login': self.oper_name.encode('utf-8'),
            'password': self.oper_pass.encode('utf-8'),
        }

