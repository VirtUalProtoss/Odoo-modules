# -*- coding: utf-8 -*-


from openerp import models, fields, api

class DirectionTypes (models.Model) :

    _name = 'data_sync.direction_types'
    name = fields.Char()
    value = fields.Char()
