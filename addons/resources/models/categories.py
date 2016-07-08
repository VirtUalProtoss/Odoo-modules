# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Categories(models.Model):
    _name = 'resources.categories'

    #type_id = fields.Integer()
    parent_id = fields.Many2one('resources.categories', 'Parent category', select=True)
    name = fields.Char(string="Title", required=True)
    caption = fields.Text()
