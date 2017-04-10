# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *
from datetime import datetime, date


class OnymaScripts(models.Model):
    _name = 'onyma.scripts'

    name = fields.Char()
    caption = fields.Text()
    sql = fields.Text()
