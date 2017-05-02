# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ObjectMapLinkRules (models.Model):
    
    _name = 'data_sync.object_map_link_rules'

    object_map_link_id = fields.Many2one('data_sync.object_map_links', 'Object Map Link', select=True)
    rule_id = fields.Many2one('data_sync.rules', 'Rule', select=True)
    #direction_type_id = fields.Many2one('data_sync.direction_types', 'Direction Type', select=True)
    order = fields.Integer()
