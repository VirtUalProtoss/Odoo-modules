# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ObjectTypes (models.Model) :
    
    name = fields.Char()
    _name = 'data_sync.object_types' # varchar

