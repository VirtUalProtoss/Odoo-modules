# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime


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

    @api.one
    @api.depends('owner_id', 'date_start')
    def create_work(self, rec):



        #self.date_comment = datetime.now()
        # self.text already stored before call function
        resource = self.env['resource.resource'].search([('user_id', '=', rec['uid'])])
        self.employee_id = 1 # administrator
        if len(resource.ids) > 0:
            employee = self.env['hr.employee'].search([('resource_id', '=', resource.ids[0])])
            if employee.id:
                self.employee_id = employee.id

        wtype = self.env['projects.work_types'].search([('name', '=', 'Обычная')])
        if wtype.id:
            type_id = wtype.id
        else:
            type_id = 1
        self.work_ids.new({
            'task_id': self.id,
            'date_start': datetime.now(),
            'owner_id': self.employee_id,
            'type_id': type_id,
        })

        view = self.reload_page()

    @api.multi
    def reload_page(self):
        model_obj = self.env['ir.model.data']
        data_id = model_obj._get_id('projects', 'work_form')
        view_id = model_obj.browse(data_id).res_id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Works',
            'res_model': 'projects.works',
            'view_type': 'tree',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'nodestroy': True,
        }

