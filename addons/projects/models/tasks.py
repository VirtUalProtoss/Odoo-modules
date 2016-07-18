# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Tasks(models.Model):
    _name = "projects.tasks"

    project_id = fields.Many2one('projects.projects', 'Project', select=True)
    owner_id = fields.Many2one('hr.employee', 'Employee', select=True)
    status_id = fields.Many2one('projects.statuses', 'Status', select=True, required=True)
    name = fields.Char()
    description = fields.Text()
    date_start = fields.Date()
    date_end = fields.Date()

    work_ids = fields.One2many('projects.works', 'task_id', string='Works', auto_join=True)

    planned_time = fields.Date(compute="get_planned_time")
    comment_ids = fields.One2many('projects.work_comments', 'work_id', compute="get_comments")

    @api.depends('work_ids.planned_time')
    def get_planned_time(self):
        for record in self:
            pdate = fields.Date().today()
            for work in record.work_ids:
                if work.planned_time:
                    if work.planned_time > pdate:
                        pdate = work.planned_time

            record.planned_time = pdate

    @api.depends('work_ids')
    def get_comments(self):
        for record in self:
            for work in record.work_ids:
                for comm in work.comment_ids:
                    self.comment_ids += comm
