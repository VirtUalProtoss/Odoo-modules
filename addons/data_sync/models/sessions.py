# -*- coding: utf-8 -*-


from openerp import models, fields, api

class Sessions (models.Model) :

    start_date = fields.Datetime()
    end_date = fields.Datetime()
    profile_id = fields.Many2one('data_sync.profiles', 'Profile', select=True)
    _name = 'data_sync.sessions' # varchar


