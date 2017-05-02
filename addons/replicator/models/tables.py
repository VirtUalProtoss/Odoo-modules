# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ReplicatorTables(models.Model):
    _name = 'replicator.tables'

    connection_id = fields.Many2one('replicator.connections', selected=True)
    name = fields.Char()

    @api.multi
    def getTables(self):
        conn = self.env['replicator.connections'].search([('operid', '=', oper.operid)])
        pass
