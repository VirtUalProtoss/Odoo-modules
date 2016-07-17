# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Projects(models.Model):
    _name = "projects.projects"

    parent_id = fields.Many2one('projects.projects', 'Parent project', select=True)
    type_id = fields.Many2one('projects.project_types', 'Type', select=True)
    owner_id = fields.Many2one('hr.employee', 'Employee', select=True)
    name = fields.Char()
    description = fields.Text()

    task_ids = fields.One2many('projects.tasks', 'project_id', string='Tasks')
