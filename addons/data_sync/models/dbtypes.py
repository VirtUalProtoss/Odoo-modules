# -*- coding: utf-8 -*-


from openerp import models, fields, api

class DBTypes (models.Model) :
    
    name = fields.Char()
    _name = 'data_sync.db_types' # vachar
