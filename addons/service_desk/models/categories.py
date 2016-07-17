# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Categories(models.Model):
    _name = "service_desk.categories"

    name = fields.Char()
    description = fields.Text()
