# -*- coding: utf-8 -*-

from openerp import models, fields, api

class OnymaServers(models.Model):
    _name = 'resources.resources'

    name = fields.Char()
    caption = fields.Text()
    address = fields.Char()
    username = fields.Char()
    password = fields.Char()
