# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Projects(models.Model):
    _name = "projects.projects"

    name = fields.Char()
    description = fields.Char()
    