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
    date_start = fields.Date()
    date_end = fields.Date()
    planned_time = fields.Date()
    planned_cost = fields.Integer()

    comment_ids = fields.One2many('projects.work_comments', 'work_id', string='Comments')
