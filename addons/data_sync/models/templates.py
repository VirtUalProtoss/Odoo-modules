# -*- coding: utf-8 -*-


from openerp import models, fields, api

class Templates (models.Model) :

    _name = 'data_sync.templates'

    name = fields.Char()
    rule_type_id = fields.Many2one('data_sync.rule_types', 'Rule Type', select=True)
    db_type_id = fields.Many2one('data_sync.db_types', 'DB Type', select=True)
    template_string = fields.Text()

    template_part_ids = fields.One2many('data_sync.template_parts', 'template_id', string='Template parts', auto_join=True)
