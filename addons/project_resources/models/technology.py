# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Technology(models.Model):
    _name = 'project.technology'

    parent_id = fields.Many2one('project.technology', 'Parent tech', select=True)
    resource_id = fields.Many2one('project.resources', 'Resource', select=True)
    name = fields.Char(string="Title", required=True)
    description = fields.Text()
