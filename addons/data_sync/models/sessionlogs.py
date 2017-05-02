# -*- coding: utf-8 -*-


from openerp import models, fields, api

class SessionLogs (models.Model) :

    session_id = fields.Many2one('data_sync.sessions', 'Session', select=True)
    object_map_id = fields.Many2one('data_sync.object_maps', 'Object Map', select=True)
    old_value = fields.Char()
    new_value = fields.Char()
    cdate = fields.Datetime()
    _name = 'data_sync.session_logs' # varchar
