# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Works(models.Model):
    _name = "projects.works"

    task_id = fields.Many2one('projects.task', 'Task', select=True)
    type_id = fields.Many2one('projects.work_types', 'Type', select=True)
    owner_id = fields.Many2one('hr.employee', 'Employee', select=True)
    after_work_id = fields.Many2one('projects.works', 'After')
    after_in_that_day = fields.Boolean(default=False)
    name = fields.Char()
    description = fields.Text()
    start_date = fields.Date()
    planned_time = fields.Integer()
    planned_cost = fields.Integer()
