# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Statuses(models.Model):
    _name = "projects.statuses"

    name = fields.Char()
    description = fields.Text()

    @api.multi
    def name_get(self):

        return [(cat.id, cat.name) for cat in self]
