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


    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        fnames = []
        for cat in self:
            fnames.append((cat.id, cat.schema_id.name + ': ' +".".join(reversed(get_names(cat)))))
        return fnames
