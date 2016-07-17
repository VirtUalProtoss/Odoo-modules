# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ProjectTypes(models.Model):
    _name = "projects.project_types"

    name = fields.Char(required=True)
