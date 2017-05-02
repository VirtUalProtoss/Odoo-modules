# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, date


class OnymaSyncRules(models.Model):
    _name = 'onyma.sync_rules'

    name = fields.Char()

    remote_table_id = fields.Integer()
    local_table_id = fields.Integer()
    field_type_id = fields.Integer()
    data_filter = fields.Char()
