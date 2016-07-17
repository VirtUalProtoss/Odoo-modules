# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Tasks(models.Model):
    _name = "projects.tasks"

    project_id = fields.Many2one('projects.projects', 'Project', select=True)
    owner_id = fields.Many2one('hr.employee', 'Employee', select=True)
    name = fields.Char()
    description = fields.Text()
    date_start = fields.Date()
