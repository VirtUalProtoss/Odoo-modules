# -*- coding: utf-8 -*-

from openerp import models, fields, api


class OnymaServers(models.Model):
    _name = 'onyma.apidogattrib'
    _table = 'apidogattrib'

    attrid = fields.Integer()
    dogid = fields.Many2one('onyma.apidoglist', 'Dogovor')
    day = fields.Datetime()
    value = fields.Text()

    def __init__(self, pool, cr):
        models.Model.__init__(self, pool, cr)
        self._auto = False

    def create(self):
        pass

    def write(self):
        pass

    def unlink(self):
        pass
