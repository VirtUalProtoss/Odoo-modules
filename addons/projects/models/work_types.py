# -*- coding: utf-8 -*-

from openerp import models, fields, api


class WorkTypes(models.Model):
    _name = "projects.work_types"

    name = fields.Char(required=True)
    description = fields.Text()
    icon = fields.Binary()

    SELF_WRITEABLE_FIELDS = [ 'image', 'image_medium', 'image_small']
    # User can read a few of his own fields
    SELF_READABLE_FIELDS = [ 'image', 'image_medium', 'image_small']
