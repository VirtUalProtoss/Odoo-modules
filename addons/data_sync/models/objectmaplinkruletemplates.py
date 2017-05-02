# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ObjectMapLinkRuleTemplates (models.Model):
    
    _name = 'data_sync.object_map_link_rule_templates'

    object_map_link_rule_id = fields.Many2one('data_sync.object_map_link_rules', 'Object Map Link Rule', select=True)
    template_id = fields.Many2one('data_sync.templates', 'Template', select=True)
    #direction_type_id = fields.Many2one('data_sync.direction_types', 'Direction Type', select=True)
    order = fields.Integer()
