# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ObjectMapRules (models.Model) :
    
    object_map_id = fields.Many2one('data_sync.object_maps', 'Object Map', select=True)
    rule_id = fields.Many2one('data_sync.rules', 'Rule', select=True)
    order = fields.Integer()
    value = fields.Char()
    part = fields.Integer() #{0: 'from', 1: 'to', } # integer
    _name = 'data_sync.object_map_rules' # varchar
