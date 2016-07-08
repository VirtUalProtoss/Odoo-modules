# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Resources(models.Model):
    _name = 'resources.resources'

    caption = fields.Text()
    template_id = fields.Many2one('resources.resource_templates', 'Resource template', select=True)
