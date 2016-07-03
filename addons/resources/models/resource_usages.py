# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResourceUsages(models.Model):
    _name = 'project.resource_usages'

    resource_id = fields.Many2one('project.resources', 'Resource', select=True)
    task_id = fields.Many2one('project.task', 'Task', select=True)
    count = fields.Integer()
    available = fields.Boolean(default=False)
