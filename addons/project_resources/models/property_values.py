# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PropertyValues(models.Model):
    _name = 'project.property_values'

    resource_id = fields.Many2one('project.resources', 'Resource', select=True)
    property_id = fields.Many2one('project.properties', 'Property', select=True)
    value = fields.Char()
    valueNum = fields.Integer()
