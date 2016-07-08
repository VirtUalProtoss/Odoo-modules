# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PropertyValues(models.Model):
    _name = 'project.property_values'

    resource_id = fields.Many2one('resources.resources', 'Resource', select=True)
    property_id = fields.Many2one('resources.properties', 'Property', select=True)
    _linked_value_id = fields.Many2one('resources.property_values', 'Linked value')
    value = fields.Char(compute='_get_value')
    real_value = fields.Char()
    value_num = fields.Integer()
    value_type = fields.Selection([
        ('V', 'Value'),
        ('DV', 'Depend Value'),
        ('MDV', 'Multi Depend Value'),
    ])

    @api.depends('real_value', 'value_type', '_linked_value_id.value')
    def _get_value(self):
        if self.value_type == 'V':
            self.value = self.real_value
        elif self.value_type == 'DV':
            self.value = self._linked_value_id.value
        elif self.value_type == 'MDV':
            # TODO: process the value_num
            self.value = self._linked_value_id.value
        else:
            self.value = None

    @api.onchange('value')
    def _onchange_value(self):
        if self.value_type == 'V':
            self.real_value = self.value
        elif self.value_type == 'DV':
            self.real_value = self.search([('value_type', '=', 'V'), ('real_value', '=', self.value)], limit=1).id
        elif self.value_type == 'MDV':
            # TODO: process the value_num
            self.real_value = self.search([('value_type', '=', 'V'), ('real_value', '=', self.value)], limit=1).id
        else:
            self.value = None
