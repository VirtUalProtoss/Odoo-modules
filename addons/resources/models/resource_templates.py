# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ResourceTemplates(models.Model):
    _name = 'resources.resource_templates'

    category_id = fields.Many2one('resources.categories', 'Category', select=True)
    name = fields.Char(string="Title", required=True)
    caption = fields.Text()
