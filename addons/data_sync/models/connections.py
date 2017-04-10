# -*- coding: utf-8 -*-


from openerp import models, fields, api

class Connections (models.Model) :

    name = fields.Char()
    ext_dbsource_id = fields.Many2one('base.external.dbsource', 'External DB Source', select=True)
    comment = fields.Char()
    db_type_id = fields.Many2one('data_sync.db_types', 'DB Type', select=True)
    _name = 'data_sync.connections' # varchar
