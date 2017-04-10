# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ConnectionRules (models.Model) :
    
    _name = 'data_sync.connection_rules'
    rule_id = fields.Many2one('data_sync.rules', 'Rule', select=True)
    connection_id = fields.Many2one('data_sync.connections', 'Connection', select=True)
    profile_id = fields.Many2one('data_sync.profiles', 'Profile', select=True)
    order = fields.Integer()
    value = fields.Char()
