# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Works(models.Model):
    #_name = "projects_resources.works"
    _inherit = "projects.works"

    resource_ids = fields.One2many('projects_resources.works_resources', 'work_id', string="Resources")
    resource_count = fields.Integer(default=0)
