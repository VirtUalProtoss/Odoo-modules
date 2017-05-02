# -*- coding: utf-8 -*-

from openerp import models, fields, api

from datetime import datetime


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


    @api.one
    @api.depends('owner_id', 'date_start', 'type_id', 'status_id', 'task_id')
    def add_work(self, rec):
        resource = self.env['resource.resource'].search([('user_id', '=', rec['uid'])])

        if rec['active_model'] == 'projects.tasks':
            task_id = rec['active_id']
        else:
            task_id = None
        self.task_id = task_id

        if not self.owner_id:

            if len(resource.ids) > 0:
                employee = self.env['hr.employee'].search([('resource_id', '=', resource.ids[0])])
                if employee.id:
                    self.owner_id = employee.id

        if not self.type_id:
            wtype = self.env['projects.work_types'].search([('name', '=', 'Обычная')])
            if wtype.id:
                self.type_id = wtype.id
            else:
                self.type_id = 1

        if not self.status_id:
            status = self.env['projects.statuses'].search([('name', '=', 'Новый')])
            if status.id:
                self.status_id = status.id
            else:
                self.status_id = 1

        if not self.date_start:
            self.date_start = datetime.now()

        #return {'type': 'ir.actions.act_window_close'}

        return self.reload_page()

    @api.multi
    def reload_page(self):
        model_obj = self.env['ir.model.data']
        data_id = model_obj._get_id('projects', 'task_form')
        view_id = model_obj.browse(data_id).res_id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'res_model': 'projects.tasks',
            'view_type': 'tree',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
