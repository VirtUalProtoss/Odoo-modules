# -*- coding: utf-8 -*-


from openerp import models, fields, api

from ..syncer import Syncer


class Profiles (models.Model) :

    _name = 'data_sync.profiles'
    
    name = fields.Char()
    sync_cron = fields.Char()
    last_start = fields.Datetime()
    last_end = fields.Datetime()

    profile_map_ids = fields.One2many('data_sync.profile_maps', 'profile_id', string='Profile maps', auto_join=True)

    @api.one
    def test(self):
        sync = Syncer()
        
