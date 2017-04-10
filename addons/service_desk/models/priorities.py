# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Priorities(models.Model):
    _name = "service_desk.priorities"

    name = fields.Char()
    description = fields.Text()
    planned_time = fields.Datetime()

    '''
    Selection([
        ('C', 'Critical'),
        ('E', 'High'),
        ('D', 'Average'),
        ('W', 'Normal'),
        ('W', 'Below Normal'),
        ('W', 'Low'),
        ('W', 'Very Low'),
    ], default='C')
    '''
