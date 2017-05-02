# -*- coding: utf-8 -*-


from openerp import models, fields, api

class TemplateParts (models.Model) :

    _name = 'data_sync.template_parts'

    template_id = fields.Many2one('data_sync.templates', 'Template', select=True)
    param_name = fields.Char()
    position = fields.Integer()
    value = fields.Char()
