# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PropertyTypes(models.Model):
    _name = 'resources.property_types'

    #parent_id = fields.Integer()
    name = fields.Char(string="Title", required=True)
