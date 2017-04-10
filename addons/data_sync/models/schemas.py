# -*- coding: utf-8 -*-


from openerp import models, fields, api

class Schemas (models.Model) :

    name = fields.Char()
    _name = 'data_sync.schemas' # varchar
