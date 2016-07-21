# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *
from datetime import date


class ApiDogList(models.Model):

    dogtypes = {
        'fl': [25, ],
        'yl': [26, ],
    }

    _name = 'onyma.api_dog_list'
    _table = 'onyma.api_dog_list'

    def create(self):
        pass

    def write(self):
        pass

    def unlink(self):
        pass

    #id = fields.Integer(related='dogid')
    dogid = fields.Integer()
    bill = fields.Integer()
    gid = fields.Integer()
    dogcode = fields.Char()
    status = fields.Integer()
    startdate = fields.Date()
    enddate = fields.Date()
    status_date = fields.Date()
    tsid = fields.Integer()
    csid = fields.Integer()
    utid = fields.Integer()

    name = fields.Char(compute='get_client_name', client='Клиент', store=True)
    dog_type = fields.Char(compute='get_dogtype', string='Тип договора')
    payment_ids = fields.One2many('onyma.payments', 'client_id')


    @api.one
    def get_dogtype(self):
        if self.utid == 25:
            self.dog_type = 'ФЛ'
        elif self.utid == 26:
            self.dog_type ='ЮЛ'
        else:
            self.dog_type = self.utid

    @api.one
    @api.depends('utid')
    def get_client_name(self):
        #if not self.client_name:
        #    if len(str(self.client_name).strip()) > 0:
        #        return
        if self.utid in self.dogtypes['fl']:
            attrid = 291
        elif self.utid in self.dogtypes['yl']:
            attrid = 12
        else:
            attrid = 12
        name = self.get_add_dog_attrib(attrid)
        self.name = name
        return name

    @api.one
    def get_add_dog_attrib(self, attrid, pdate=date.today(), format=('%Y-%m-%d', 'yyyy-mm-dd')):
        rec = self.env['onyma.servers'].search([('name', '=', 'ЦБ ТТК')])
        auth_params = rec.get_auth_params()[0]
        conn = connection(rec, auth_params)
        sql = '''
            select value
            from api_dog_attrib
            where
                dogid = %(dogid)d
                and attrid = %(attrid)d
                and day = to_date('%(pdate)s', '%(format)s')
        '''

        result = conn.exec_sql(sql %({
            'dogid': self.dogid,
            'attrid': attrid,
            'pdate': pdate.strftime(format[0]),
            'format': format[1],
        }))
        recs = get_db_data(result)
        print 'Process client name'
        client_name = None
        for rec in recs:
            print 'attr', attrid, 'is', rec['value']
            client_name = rec['value']

        return client_name
