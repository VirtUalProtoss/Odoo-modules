# -*- coding: utf-8 -*-


from openerp import models, fields, api

class RuleTypes (models.Model) :
    
    name = fields.Char()
    executor_func = fields.Char()
    object_type_id = fields.Many2one('data_sync.object_types', 'Object Type', select=True)
    _name = 'data_sync.rule_types' # varchar

