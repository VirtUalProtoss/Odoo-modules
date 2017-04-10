# -*- coding: utf-8 -*-


from openerp import models, fields, api

class Rules (models.Model) :
    
    name = fields.Char()
    rule_type_id = fields.Many2one('data_sync.rule_types', 'Type', select=True)
    value = fields.Char()
    _name = 'data_sync.rules' # varchar
