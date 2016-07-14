# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Resources(models.Model):
    _name = 'resources.resources'

    template_id = fields.Many2one('resources.resource_templates', 'Resource template', select=True)
    name = fields.Char()
    caption = fields.Text()

    property_ids = fields.One2many('resources.property_values', 'resource_id', string='Properties')
    template_property_ids = fields.One2many('resources.resource_properties', 'template_id', string='Template Properties')

    @api.onchange('template_id')
    def _fill_properties(self):
        if self.id:
            self.caption = self.template_id.name
            #props = ['properties_case_type', 'properties_model']
            for prop in self.template_id.property_ids:
                self.env['resources.property_values'].create({
                    'resource_id': self.id,
                    'property_id': prop.property_id.id,
                    'name': prop.property_id.name,
                })
                self.caption += ' ' + prop.property_id.name
