# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Incidents(models.Model):
    _name = "service_desk.incidents"

    category_id = fields.Many2one('service_desk.categories', 'Category', select=True, required=True)
    type_id = fields.Many2one('service_desk.types', 'Type', select=True, required=True)
    customer_id = fields.Many2one('hr.employee', 'Employee', select=True, required=True)
    executor_id = fields.Many2one('hr.employee', 'Employee', select=True)
    name = fields.Char()
    description = fields.Text()
    start_date = fields.Date()
    end_date_limit = fields.Date()
    cause_type = fields.Selection([
        ('C', 'Consult'),
        ('E', 'Error'),
        ('D', 'Develop'),
        ('W', 'Want'),
    ], default='C', required=True)
    priority_id = fields.Many2one('service_desk.priorities', 'Priority', select=True, required=True)
