# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Projects(models.Model):
    _name = "projects.projects"

    parent_id = fields.Many2one('projects.projects', 'Parent project', select=True)
    type_id = fields.Many2one('projects.project_types', 'Type', select=True)
    owner_id = fields.Many2one('hr.employee', 'Employee', select=True)
    status_id = fields.Many2one('projects.statuses', 'Status', select=True, required=True)
    name = fields.Char()
    description = fields.Text()

    task_ids = fields.One2many('projects.tasks', 'project_id', string='Tasks')

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]
