# -*- coding: utf-8 -*-


from openerp import models, fields, api

class ObjectMaps (models.Model):

    _name = 'data_sync.object_maps'

    profile_map_id = fields.Many2one('data_sync.profile_maps', 'Profile Map', select=True)
