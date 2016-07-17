# -*- coding: utf-8 -*-

from openerp import models, fields, api


class WorkComments(models.Model):
    _name = "projects.work_comments"

    work_id = fields.Many2one('projects.works', 'Work', select=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', select=True)
    text = fields.Text()
