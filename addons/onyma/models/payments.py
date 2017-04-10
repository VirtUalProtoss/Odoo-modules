# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *


class OnymaPayments(models.Model):
    _name = 'onyma.payments'

    cdate = fields.Datetime()
    mdate = fields.Datetime()
    idate = fields.Datetime()
    billdate = fields.Datetime()
    amountr = fields.Float()
    amount = fields.Float()
    currencyid = fields.Integer()
    coef = fields.Integer()
    dogid = fields.Integer()
    #dogid = fields.Many2one('onyma.apidoglist', 'Dogovor', select=True)
    client_id = fields.Many2one('onyma.apidoglist', 'Dogovor', select=True)
    ntype = fields.Integer()
    ppid = fields.Integer()
    paydoc = fields.Text()
    payed = fields.Integer()
    rmrk = fields.Text()
    operid = fields.Many2one('onyma.operators', 'Operator', select=True)
    bcid = fields.Integer()
    ppdate = fields.Datetime()
    row_id = fields.Char()
