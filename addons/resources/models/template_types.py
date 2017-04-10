# -*- coding: utf-8 -*-

from openerp import models, fields, api

class TemplateTypes(models.Model):
    _name = 'resources.template_types'

    name = fields.Char(string="Title", required=True)
    module_name = fields.Char(required=True)
    caption = fields.Text()
