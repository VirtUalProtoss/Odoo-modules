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
    ntype = fields.Integer()
    ppid = fields.Integer()
    paydoc = fields.Char()
    payed = fields.Integer()
    rmrk = fields.Text()
    operid = fields.Many2one('onyma.operators', 'Operator', select=True)
    bcid = fields.Integer()
    ppdate = fields.Integer()
    rowid = fields.Char()
