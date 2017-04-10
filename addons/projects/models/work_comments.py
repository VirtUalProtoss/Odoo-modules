# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime


class WorkComments(models.Model):
    _name = "projects.work_comments"

    work_id = fields.Many2one('projects.works', 'Work', select=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', select=True)
    date_comment = fields.Datetime()
    text = fields.Text()


    @api.one
    @api.depends('work_id', 'employee_id', 'date_comment', 'text')
    def add_comment(self, rec):
        if rec['active_model'] == 'projects.works':
            work_id = rec['active_id']
        else:
            work_id = None
        self.work_id = work_id
        self.date_comment = datetime.now()
        # self.text already stored before call function
        resource = self.env['resource.resource'].search([('user_id', '=', rec['uid'])])
        if len(resource.ids) > 0:
            employee = self.env['hr.employee'].search([('resource_id', '=', resource.ids[0])])
            if employee.id:
                self.employee_id = employee.id

        return {'type': 'ir.actions.act_window_close'}
