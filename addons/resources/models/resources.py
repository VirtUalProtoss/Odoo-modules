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
        #if self.id:
        self.caption = self.template_id.name
        #props = ['properties_case_type', 'properties_model']
        for prop in self.template_id.property_ids:
            #self.env['resources.property_values'].create({
            self.property_ids += self.property_ids.new({
                #self.property_ids.create({
                'resource_id': models.NewId,
                'property_id': prop.property_id.id,
                #'name': prop.name,
            })
            self.caption += ' ' + prop.name
        self.reload_page()

    @api.multi
    def reload_page(self):
        model_obj = self.env['ir.model.data']
        data_id = model_obj._get_id('resources', 'resources_form_view')
        view_id = model_obj.browse(data_id).res_id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Properties',
            'res_model': 'resources.property_values',
            'view_type': 'tree',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
