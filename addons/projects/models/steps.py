# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Steps(models.Model):
    _name = "projects.steps"

    work_id = fields.Many2one('projects.works', 'Work', select=True)
    name = fields.Char()
    description = fields.Text()
