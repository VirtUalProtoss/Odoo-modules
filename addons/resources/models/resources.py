# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Resources(models.Model):
    _name = 'resources.resources'

    template_id = fields.Many2one('resources.resource_templates', 'Resource template', select=True)
    name = fields.Char()
    caption = fields.Text()

    property_ids = fields.One2many('resources.property_values', 'resource_id', string='Properties')

