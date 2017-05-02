# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Storages(models.Model):
    _name = 'storage.storages'

    parent_id = fields.Many2one('storage.storages', 'Parent storage', select=True)
    name = fields.Char(string="Title", required=True)
    caption = fields.Text()
    #address = fields.Many2one('storage.storages', 'Parent storage', select=True)

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]
