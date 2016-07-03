# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Blueprint(models.Model):
    _name = 'project.blueprint'

    name = fields.Char(string="Title", required=True)
    resource_id = fields.Many2one('project.resources', 'Resource', select=True)
    file_name = fields.Char()
    file_format = fields.Char()
    description = fields.Text()
