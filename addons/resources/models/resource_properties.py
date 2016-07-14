# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ResourceProperties(models.Model):
    _name = 'resources.resource_properties'

    template_id = fields.Many2one('resources.resource_templates', 'Resource template', select=True)
    property_id = fields.Many2one('resources.properties', 'Property', select=True)

    name = fields.Char(string="Title", required=True)
    caption = fields.Text()

    @api.multi
    def name_get(self):
        def get_names(cat):
            """ Return the list [cat.name, cat.parent_id.name, ...] """
            res = []
            while cat:
                res.append(cat.name)
                cat = cat.parent_id
            return res

        return [(cat.id, cat.template_id.name + " - " + cat.name) for cat in self]
