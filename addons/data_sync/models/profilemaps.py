# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ProfileMaps (models.Model):

    _name = 'data_sync.profile_maps'

    profile_id = fields.Many2one('data_sync.profiles', 'Profile', select=True)
    connection_id = fields.Many2one('data_sync.connections', 'Connection', select=True)
    direction_type_id = fields.Many2one('data_sync.direction_types', 'Direction Type', select=True)
    get_data_cache = fields.Char()
    set_data_cache = fields.Char()
    process_data_cache = fields.Char()
    schema_id = fields.Many2one('data_sync.schemas', 'Schema', select=True)

    
