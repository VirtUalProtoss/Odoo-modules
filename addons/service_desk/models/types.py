# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Types(models.Model):
    _name = "service_desk.types"

    task_id = fields.Many2one('projects.task', 'Task', select=True)
    administrator_id = fields.Many2one('hr.employee', 'Employee', select=True)
    name = fields.Char()
    description = fields.Text()
