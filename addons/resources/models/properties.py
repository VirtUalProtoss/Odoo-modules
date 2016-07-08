# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Properties(models.Model):
    _name = 'resources.properties'

    #type_id = fields.Integer()
    type_id = fields.Many2one('resources.property_types', 'Property type', select=True)
    length = fields.Integer()
    accuracy = fields.Integer()
    unique = fields.Boolean()
    value = fields.Char()
    default_value = fields.Char()
    is_list = fields.Boolean()
    is_inheritable = fields.Boolean()
    name = fields.Char(string="Title", required=True)
    caption = fields.Text()
