# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Categories(models.Model):
    _name = 'resources.categories'

    parent_id = fields.Many2one('resources.categories', 'Parent category', select=True)
    name = fields.Char(string="Title", required=True)
    caption = fields.Text()

    '''
    parent_left = fields.Integer('Left Parent', select=1),
    parent_right = fields.Integer('Right Parent', select=1),


    _parent_name = 'parent_id'
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
    '''



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

    #@api.multi
    #def _rec_name(self):
    #    def get_names(cat):
    #        """ Return the list [cat.name, cat.parent_id.name, ...] """
    #        res = []
    #        while cat:
    #            res.append(cat.name)
    #            cat = cat.parent_id
    #        return res

    #    return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]


    #def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
    #    res = self.name_get(cr, uid, ids, context=context)
    #    return dict(res)

