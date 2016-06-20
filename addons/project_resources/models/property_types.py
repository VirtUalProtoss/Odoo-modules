# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PropertyTypes(models.Model):
    _name = 'project.property_types'

    #parent_id = fields.Integer()
    parent_id = fields.Many2one('project.property_types', 'Parent type', select=True)
    name = fields.Char(string="Title", required=True)
    caption = fields.Text()
