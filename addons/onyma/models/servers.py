# -*- coding: utf-8 -*-

from openerp import models, fields, api
from ..connection import *
from ..billing.onyma import Onyma
from ..billing.onyma.bills import Bills
from datetime import datetime, date


class OnymaServers(models.Model):
    _name = 'onyma.servers'

    name = fields.Char()
    caption = fields.Text()
    engine = fields.Char()
    host = fields.Char()
    port = fields.Integer()
    database = fields.Char()
    encoding = fields.Char()
    username = fields.Char()
    password = fields.Char()
    auth_sql = fields.Char()

    oper_name = fields.Char()
    oper_pass = fields.Char()

    @api.one
    def get_auth_params(self):
        return {
            'login': self.oper_name.encode('utf-8'),
            'password': self.oper_pass.encode('utf-8'),
        }

    @api.one
    @api.depends('caption')
    def check_connect(self):
        auth_params = self.get_auth_params()[0]
        conn = connection(self, auth_params)
        test_sql = '''
            select operid from api_operators where login = '%s'
        '''

        result = conn.exec_sql(test_sql % (auth_params['login'], ))
        self.caption = str(get_db_data(result))

    @api.one
    def get_onyma_operators(self):
        auth_params = self.get_auth_params()[0]
        conn = connection(self, auth_params)

        obj = Onyma(conn.get_session())
        operators = obj.get_operators_by_gid(24193)
        for oper in operators:
            odoo_oper = self.env['onyma.operators'].search([('operid', '=', oper.operid)])
            if not odoo_oper.id:
                self.env['onyma.operators'].create({
                    'operid': oper.operid,
                    'name': oper.name,
                    'login': oper.login,
                    'gid': oper.gid,
                    'email': oper.email
                })

    @api.one
    def get_onyma_payments(self, pdate=date.today()):
        auth_params = self.get_auth_params()[0]
        conn = connection(self, auth_params)

        day = date.today().strftime('%d.%m.%y')

        sql = '''
                select
                    ad.ROWID row_id
                    , ad.cdate
                    , adl.gid
                    , ad.dogid
                    , ad.bcid
                    , ad.ppdate
                    , ad.operid
                    , ad.amount
                    , ad.billid
                    , ad.rmrk
                    , ad.ntype
                    , ad.paydoc
                    , adl.dogcode
                from api_dogpayment ad
                join api_dog_list adl on ad.dogid = adl.dogid
                where
                    1 = 1
                    and adl.gid = 24193
                    and ad.cdate between to_date('%s 00:00:00', 'dd.mm.yy HH24:MI:SS')
                            and to_date('%s 23:59:59', 'dd.mm.yy HH24:MI:SS')
            ''' % (day, day, )
        print 'Getting payments'
        result = conn.exec_sql(sql)
        recs = get_db_data(result)

        #recs = obj.get_bills({'gid': 24193, 'mdate': {'check_type': '>=', 'value': date.today()}, })
        print 'Process payments'
        for rec in recs:
            client = self.env['onyma.api_dog_list'].search([('dogid', '=', rec['dogid'])])

            if not client.id:
                print 'dogcode', rec['dogcode'], 'out of api_dog_list'
                continue

            operator = self.env['onyma.operators'].search([('operid', '=', rec['operid'])])
            if not operator.id:
                print 'operator', rec['operid'], 'out of operators'
                continue

            odoo_rec = self.env['onyma.payments'].search([('row_id', '=', rec['row_id'])])

            if not odoo_rec.id:
                print 'Write new payments', rec
                try:
                    self.env['onyma.payments'].create({
                        'row_id': rec['row_id'],
                        'cdate': rec['cdate'].strftime('%Y-%m-%d %H:%M:%S'),
                        'gid': rec['gid'],
                        'dogid': rec['dogid'],
                        'bcid': rec['bcid'],
                        'ppdate': rec['ppdate'].strftime('%Y-%m-%d'),
                        'operid': operator.id,
                        'amount': rec['amount'],
                        'client_id': client.id,
                        'billid': rec['billid'],
                        'rmrk': rec['rmrk'],
                        'ntype': rec['ntype'],
                        'paydoc': str(rec['paydoc']),
                    })
                except Exception, e:
                    print 'Error in rec', rec['row_id']
                    print e

    def user_auth(self):
        pass

    @api.one
    def get_onyma_dogs(self):
        auth_params = self.get_auth_params()[0]
        conn = connection(self, auth_params)

        sql = '''
            select
                dogid
                , bill
                , gid
                , dogcode
                , status
                , startdate
                , enddate
                , status_date
                , tsid
                , csid
                , utid
            from api_dog_list
            where gid = 24193

            and dogcode in (
                '233044775','233045051','233079421','233079657','233064104','233651655','233074335','233672472',
                '233033260','233029330','233029330','233029330','233029515','233029975','233029975','233029975',
                '233030758','233030758','233033258','233033258','233033259','233033259','233035307','233035307',
                '233035307','233035843','233035843','233035843','233036482','233036482','233036482','233059650',
                '233059650','233059650','233063132','233064069','233075626','233080116','233080706','233080706',
                '233080706','233075554','233075414','233077920','233030509','233064224','233030187','233077885',
                '233030188','233080644','233035776','233062190','233062190','233062190','233077615','233029226',
                '233029226','233029226','233080540','233031229','233034272','233035402','233035402','233030537',
                '233060938','233075351','233616158','233027908','233079368','233079369','233032931','233029566',
                '233034236','233034236','233077391','233702387','233035655','233035655','233656066','233033974',
                '233078805','233036949','233036949','233078005','233035800','233037179','233037179','233055979',
                '233062157','233030145','233030145','233059579','233034938','233034938','233059579','233035552',
                '233035552','233080118','233078637','233077792','233051807','233064607','233064607','233064607',
                '233034824','233031635','233030347','233030347','233051680','233035785','233035785','233078820',
                '233658027','233036552','233714259','233714259','233034247','233036687','233036687','233036687',
                '233036715','233061602','233051807','233026006','233713663','233714259','233063687','233063687',
                '233056186','233031097','233031697','233031697','233031697','233031214','233030563','233051945',
                '233030608','233029688','233029688','233080128','233034389','233034389','233034389','233063195',
                '233063196','233031335','233035631','233035631','233035819','233078797','233034742','233032620',
                '233032620','233032620','233052967','233076435','233077668','233030895','233076871','233030779',
                '233030779','233034271','233034271','233680240','233713564','233036651','233036651','233036651',
                '233036651','233585801','233080654','233080654','233080654','233645024','233036674','233025986',
                '233025986','233025986','233029138','233062591','233029138','233030263','233034402','233062676',
                '233033211','233033211','233036796','233075817','233075817','233075817','233037368','233037368',
                '233037368','233037459','233080458','233080437','233079238','233079239','233714166','233037437',
                '233037437','233034617','233035590','233035590','233063584','233063584','233063584','233029712',
                '233713719','233080381','233029151','233029128','233051558','233065421','233031323','233030022',
                '233032240','233032240','233032969','233032969','233064688','233064688','233064688','233037404',
                '233077845','233052480','233031637','233031637','233031290','233031290','233064976','233064977',
                '233032026','233072566','233072566','233072567','233031898','233031898','233036398','233036398',
                '233053357','233078639','233037429','233079399','233079399','233060957','233030434','233037258',
                '233036698','233059249','233079383','233036290','233036290','233077490','233079380','233036991',
                '233036991','233079385','233079385','233714215','233031281','233078033','233078031','233078031',
                '233714256','233029999','233029999','233029999','233036748','233080515','233036283','233030428',
                '233030190','233610085','233714172','233056234','233056234','233056234','233034231','233034231',
                '233051638','233029849'
            )
        '''
        print 'Getting clients'
        result = conn.exec_sql(sql)
        recs = get_db_data(result)
        print 'Process clients', len(recs)
        for rec in recs:
            odoo_rec = self.env['onyma.api_dog_list'].search([('dogid', '=', rec['dogid'])])
            if not odoo_rec.id:
                self.env['onyma.api_dog_list'].create(rec)
        print 'End process clients'
