# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PropertyValues(models.Model):
    _name = 'project.property_values'

    resource_id = fields.Many2one('resources.resources', 'Resource', select=True)
    property_id = fields.Many2one('resources.properties', 'Property', select=True)
    value = fields.Char()
    valueNum = fields.Integer()
    valueType = fields.Selection([
        ('V', 'Value'),
        ('DV', 'Depend Value'),
        ('MDV', 'Multi Depend Value'),
    ])
