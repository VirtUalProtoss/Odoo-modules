# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ObjectMapLinks (models.Model):

    _name = 'data_sync.object_map_links'
    
    object_map_id = fields.Many2one('data_sync.object_maps', 'Object Map', select=True)
    object_id = fields.Many2one('data_sync.objects', 'Object', select=True)
    direction_type_id = fields.Many2one('data_sync.direction_types', 'Direction Type', select=True)
