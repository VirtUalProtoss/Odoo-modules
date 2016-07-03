# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Resources(models.Model):
    _name = 'project.resources'

    type_list = fields.Selection([('Prod', 'Product'), ('Tech', 'Technology'), ('BP', 'Blueprint'), ('ProdSpec', 'Production specification')])
    caption = fields.Text()
    task_id = fields.Many2one('project.task', 'Task', select=True)
    need_count = fields.Integer()
    product_id = fields.Many2one('product.product', 'Product/component', select=True)
    technology_id = fields.Many2one('project.technology', 'Technology', select=True)
    blueprint_id = fields.Many2one('project.blueprint', 'Blueprint', select=True)
    prod_spec_id = fields.Many2one('mrp.bom', 'Production specification', select=True)
    object_id = fields.Integer()

    @api.onchange('type_list')
    def change_res(self):
        if self.type_list == 'Tech':
            self.object_id = fields.One2many('product.product', 'resource_id', string='Resource')
        elif self.type_list == 'BP':
            self.object_id = fields.One2many('project.blueprint', 'resource_id', string='Resource')
        else:
            self.object_id = fields.One2many('product.product', 'resource_id', string='Resource')
