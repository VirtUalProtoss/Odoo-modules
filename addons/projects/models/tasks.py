# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Tasks(models.Model):
    _name = "projects.tasks"

    project_id = fields.Many2one('projects.projects', 'Project', select=True)
    owner_id = fields.Many2one('hr.employee', 'Employee', select=True)
    name = fields.Char()
    description = fields.Text()
    date_start = fields.Date()
    date_end = fields.Date()

    work_ids = fields.One2many('projects.works', 'task_id', string='Works')

    planned_time = fields.Date(computed="get_planned_time")

    def get_planned_time(self):
        pdate = fields.Date().today()
        for work in self.work_ids:
            if work.planned_time:
                if work.planned_time > pdate:
                    pdate = work.planned_time
        return pdate

    def get_comments(self):
        comments = []
        for work in self.work_ids:
            for comm in work.comment_ids:
                comments.append(comm.text)
