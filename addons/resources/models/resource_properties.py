# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ResourceProperties(models.Model):
    _name = 'resources.resource_properties'

    template_id = fields.Many2one('resources.resource_templates', 'Resource template', select=True)
    property_id = fields.Many2one('resources.properties', 'Property', select=True)

    name = fields.Char(string="Title", required=True)
    caption = fields.Text()
