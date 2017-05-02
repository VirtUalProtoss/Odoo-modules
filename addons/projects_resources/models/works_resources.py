# -*- coding: utf-8 -*-

from openerp import models, fields, api


class WorksResources(models.Model):
    _name = "projects_resources.works_resources"

    work_id = fields.Many2one('projects.works', 'Work', select=True, required=True)
    resource_id = fields.Many2one('resources.resources', 'Resource', select=True, required=True)
    need_count = fields.Integer()
