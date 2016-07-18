# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Works(models.Model):
    _name = "projects.works"

    task_id = fields.Many2one('projects.tasks', 'Task', select=True)
    status_id = fields.Many2one('projects.statuses', 'Status', select=True, required=True)
    type_id = fields.Many2one('projects.work_types', 'Type', select=True)
    owner_id = fields.Many2one('hr.employee', 'Employee', select=True)
    after_work_id = fields.Many2one('projects.works', 'After')
    after_in_that_day = fields.Boolean(default=False)
    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    date_start = fields.Date(string='Star date')
    date_end = fields.Date(string='End date')
    planned_time = fields.Date(string='Planned time')
    planned_cost = fields.Integer(string='Planned cost')

    comment_ids = fields.One2many('projects.work_comments', 'work_id', string='Comments')
