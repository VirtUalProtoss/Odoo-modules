# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Properties(models.Model):
    _name = 'project.properties'

    #type_id = fields.Integer()
    type_id = fields.Many2one('project.property_types', 'Property type', select=True)
    name = fields.Char(string="Title", required=True)
    caption = fields.Text()
