# -*- coding: utf-8 -*-

__author__ = 'virtual'

from .. import Onyma
from datetime import date

from miscHelper.functions import get_db_data

from schema.onyma.apibills import ApiBills
from schema.onyma.apidogpayment import ApiDogpayment
from schema.onyma.apimonthbills import ApiMonthBills
from schema.onyma.apibilltype import ApiBillType
from schema.onyma.apioperators import ApiOperators
from schema.onyma.apitimecredit import ApiTimeCredit

from sqlalchemy.sql import func
from datetime import datetime



import cx_Oracle


class Bills(Onyma):


    def __init__(self, session):
        Onyma.__init__(self, session)

    def insert_bill_other(self, payment):
        sql = '''
            declare
                lbillid number;
            begin
                begin
                    lbillid := o_mdb.api_change_dog.ins_bill_others(:pbill, :pdate, :pamount, :pntype, :premark, :pbcid);
                    commit;
                exception
                    when others then rollback;
                end;
            end;
        '''
        return self.session.execute(sql, payment)

    def del_bill_other(self, rowid):
        sql = '''
            begin
               o_mdb.api_change_dog.del_bill_others(:prowid);
               commit;
            exception
               when others then rollback;
            end;
        '''
        self.exec_function(sql, {'prowid': rowid, })

    def get_bills_rowid(self, payment):
        sql = '''
            select
                ROWID
            from api_bills ab
            where
                1 = 1
                and ab.bill = :pbill
                and ab.ntype = :pntype
                and ab.mdate = :pdate
                and ab.amount = :pamount
                and ab.bcid = :pbcid
                and ab.remark = :premark
        '''
        return self.session.execute(sql, payment)

    def get_bill_remainder(self, bill, l_date=date.today()):
        sql = '''
            select o_mdb.api_func.get_remainder(:pbill, :pdate) amount from dual
        '''
        res = self.exec_function(sql, {
            'pbill': bill,
            'pdate': l_date,
        })
        balances = get_db_data(res)
        balance = 0
        for row in balances:
            balance += row['amount']

        return balance

    def get_bcid_remainder(self, bill, bcid, l_date=date.today()):
        sql = '''
            select o_mdb.api_func.get_bcid_remainder(:pbill, :pbcid, :pignore_bcid, :pdate) amount from dual
        '''
        res = self.exec_function(sql, {
            'pbill': bill,
            'pbcid': bcid,
            'pignore_bcid': 0,
            #'bdate': "to_date('%s', 'dd.mm.yyyy')" % (l_date.strftime('%d.%m.%Y'), ),
            'pdate': l_date,
        })
        balances = get_db_data(res)
        balance = 0
        for row in balances:
            balance += row['amount']

        return balance

    def get_bills(self, params={}):
        q = self.session.query(ApiBills)
        try:
            q = self.get_parametrized_filter(ApiBills, q, params)
        except:
            pass
        return q.all()

    def get_payments_w_info(self, params={}, gparams={}):
        sql = '''
            select
                *
            from (
                select
                    pays.*
                    , decode(
                        pays.bcid,
                        0, decode(pays.vdog, 'Интернет', 1, 'Телевидение', 1, -1),
                        24, decode(pays.vdog, 'Телефония', 2, 'LM', 3, 'Канал связи', 3, 'Прочие услуги НТ', 3, -1),
                        25, decode(pays.vdog, 'Телефония', 2, -1),
                        23, decode(pays.vdog, 'Телефония', 2, -1),
                        22, decode(pays.vdog, 'Телефония', 5, -1),
                        29, decode(pays.vdog, 'Телефония', 4, -1),
                        26, decode(pays.vdog, 'Телефония', 6, -1),
                        27, decode(pays.vdog, 'Телефония', 7, -1),
                        -1
                    ) section
                from (
                    select
                        nvl(ab.cdate, ab.mdate) cdate
                        , ab.billid
                        , ab.mdate
                        , round(ab.amount, 2) amount
                        , ab.ntype
                        , abt.remark bill_type
                        , ab.bcid
                        , ab.operid
                        , ao.name oper_name
                        , ab.dogid
                        , adl.dogcode
                        , adl.utid
                        , ab.rmrk rmrk
                        --, nvl(di.f4, api_func.get_add_dog_attrib(ab.dogid, 364, sysdate)) vdog
                        , nvl(api_func.get_add_dog_attrib(ab.dogid, 364, sysdate), 'Интернет') vdog
                        --, nvl(di.f5, decode(adl.utid, 25, api_func.get_add_dog_attrib(adl.dogid, 291, sysdate), 26, api_func.get_add_dog_attrib(adl.dogid, 12, sysdate))) client
                        , decode(adl.utid, 25, api_func.get_add_dog_attrib(adl.dogid, 291, sysdate), 26, api_func.get_add_dog_attrib(adl.dogid, 12, sysdate)) client
                        , round(nvl(api_func.get_remainder(adl.dogid, sysdate), 0.0), 2) remainder
                    from api_dogpayment ab
                    join api_dog_list adl on ab.dogid = adl.dogid
                    join api_bill_type abt on ab.ntype = abt.ntype
                    join api_operators ao on ab.operid = ao.operid
                    --right outer join UAPI_V_QUERY_17441 di on di.f1 = ab.dogid
                    where
                        1 = 1
                        %(params)s
                ) pays
            )
            where
                1 = 1
                %(gparams)s
        '''.decode('utf-8')
        param_str = ''
        param_data = {}
        gparam_str = ''
        gparam_data = {}
        if len(params) > 0:
            param_str, param_data = self.fill_params(params)
        if len(gparams) > 0:
            gparam_str, gparam_data = self.fill_params(gparams)
        nsql = sql % ({
            'params': param_str,
            'gparams': gparam_str,
        })
        sparams = {}
        sparams.update(param_data)
        sparams.update(gparam_data)
        return self.session.execute(nsql, sparams)

    def get_month_bills(self, params={}):
        q = self.session.query(ApiMonthBills)
        q = self.get_parametrized_filter(ApiMonthBills, q, params)
        return q.all()

    def get_time_credit(self, dogid, c_date, params={}):
        q = self.session.query(ApiTimeCredit)
        q = q.filter(ApiTimeCredit.dogid==dogid)
        q = self.get_parametrized_filter(ApiTimeCredit, q, params)
        sql = '''
            select * from api_time_credit where dogid = :dogid and mdate >= :mdate
        '''
        return self.exec_function(sql, {'dogid': dogid, 'mdate': c_date,})
        #return q.all()

    def ins_pay(self, dogid, summa, bcid=24, use_pay_prior=1, ppid=150, currid=2, cdate=datetime.now(), remark=''):
        # ppid number := 150; -- наличные
        sql = '''
            --declare
            --    pint number;
            begin
            :pint := o_mdb.api_pay.ins_pay(
                pdogid => :pdogid,
                pamount => :pamount,
                pbdate => :pcdate,
                pmdate => :pcdate,
                pidate => :pcdate,
                ppaydoc => '',
                pppdate => :pcdate,
                premark => :premark,
                pcurrid => :pcurrid,
                pppid => :pppid,
                pbcid => :pbcid,
                puse_pay_prior => :puse_pay_prior
            );
            end;
        '''
        params = {
            'pdogid': dogid,
            'pamount': summa,
            'pcdate': cdate,
            #'pmdate': cdate,
            #'pidate': cdate,
            #'ppaydoc': '',
            'pppdate': cdate,
            'premark': remark,
            'pcurrid': currid,
            'pppid': ppid,
            #'pbilldoc': None,
            #'pconvcurr': None,
            #'pactive_date': None,
            'pbcid': bcid,
            #'pbill': None,
            'puse_pay_prior': use_pay_prior,
            'pint': 0,
        }

        result = self.session.execute(sql, params)
        #billid = cx_Oracle.NUMBER
        #return billid
        #result = self.exec_procedure(sql, params)
        return result

    def exec_procedure(self, proc_name, params):
        cursor = self.db_conn.get_cursor()
        v_Vars = cursor.setinputsizes(pint = cx_Oracle.NUMBER)
        cursor.execute(proc_name, params)
        return v_Vars["pint"].getvalue()

    def ins_auto_pay(self, summa, bcid=None):
        sql = '''
            begin
                o_mdb.
            end;
        '''
        if bcid:
            pass

    def get_bills_group(self, params={}):
        q = self.session.query(
            ApiBills.operid, #.name.label('Оператор'),
            ApiOperators.name.label('Operator'),
            ApiBills.mdate.label('Date'),
            ApiBills.ntype,
            ApiBillType.remark.label('NType'),
            func.sum(ApiBills.amount).label('Summa'),
            func.count(ApiBills.amount).label('Count')
        )
        #q = self.session.query(ApiBills)

        q = q.join(ApiOperators)
        q = q.join(ApiBillType)
        q = self.get_parametrized_filter(ApiBills, q, params)
        q = q.group_by(ApiBills.operid, ApiOperators.name, ApiBills.mdate, ApiBills.ntype, ApiBillType.remark)
        q = q.order_by(ApiBills.mdate)
        return q.all()
