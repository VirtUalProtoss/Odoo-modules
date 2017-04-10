# -*- coding: utf-8 -*-


from openerp import models, fields, api

class DataObjects (models.Model) :

    _name = 'data_sync.objects'

    parent_id = fields.Many2one('data_sync.objects', 'Parent Object', select=True)
    object_type_id = fields.Many2one('data_sync.object_types', 'Type', select=True)
    schema_id = fields.Many2one('data_sync.schemas', 'Schema', select=True)
    name = fields.Char()

    object_map_link_ids = fields.One2many('data_sync.object_map_links', 'object_id', string='Map links')
    

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
