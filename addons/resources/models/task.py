# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Task(models.Model):
    _name = "project.task"
    _inherit = "project.task"

    resources = fields.One2many('project.resources', 'task_id', string='Resources')
