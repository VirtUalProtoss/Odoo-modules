# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, date


class OnymaScripts(models.Model):
    _name = 'onyma.remote_tables'

    name = fields.Char()
    caption = fields.Text()
    last_synced = fields.Datetime()
    sync = fields.Boolean()
