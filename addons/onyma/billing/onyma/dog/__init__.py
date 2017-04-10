# -*- coding: utf-8 -*-

__author__ = 'virtual'

from sqlalchemy import between, desc, func

from .. import Onyma
from schema.onyma.apidoglist import ApiDogList
from schema.onyma.apiauditdoglist import ApiAuditDogList
from datetime import datetime
from schema.onyma.apiclientresources import ApiClientResources
from schema.onyma.apiclientprops import ApiClientProps
from schema.onyma.query_17438 import UAPI_V_QUERY_17438 as V_Q_PHONES
from schema.onyma.query_17441 import UAPI_V_QUERY_17441 as V_Q_DOGOVORS
from schema.onyma.query_16998 import UAPI_V_QUERY_16998 as V_Q_DETAILS
from schema.onyma.apibilltypeclass import ApiBillTypeClass


class Dog(Onyma):

    def __init__(self, session):
        Onyma.__init__(self, session)

    def get_dog(self, dogcode):
        return self.get_table_data(ApiDogList, {'dogcode': dogcode, })

    def get_dogs(self, params):
        q = self.session.query(ApiDogList)
        q = self.get_parametrized_filter(ApiDogList, q, params)
        return q.all()

    def get_dog_by_vquery_phone(self, phone_number):
        q = self.session.query(V_Q_PHONES)
        q = q.filter(V_Q_PHONES.f4==phone_number)
        return q.all()

    def get_v_query_info(self, dogid):
        q = self.session.query(V_Q_DOGOVORS)
        q = q.filter(V_Q_DOGOVORS.f1==dogid)
        return q.all()

    def get_bill_type_classes(self):
        q = self.session.query(ApiBillTypeClass)
        return q.all()

    def get_v_query_phones(self, dogid):
        q = self.session.query(V_Q_PHONES.f3)
        q = q.filter(V_Q_PHONES.f3==dogid)
        return q.all()

    def get_dog_by_vquery_client(self, client):
        q = self.session.query(V_Q_DOGOVORS.f1)
        q = q.filter(func.upper(V_Q_DOGOVORS.f5).like('%' + func.upper(client) + '%'))
        return q.all()

    def get_dog_by_dogid(self, dogid):
        q = self.session.query(ApiDogList)
        q = q.filter(ApiDogList.dogid==dogid)
        return q.one()

    def block_dog(self, dogid, c_date=datetime.now()):
        sql = '''
            declare
                rres integer;
            begin
                rres := uapi_dog_status_pbo.set_dog_status(:p_dogid, :p_begdate);
                commit;
            exception
                when others then rollback;
            end;
        '''
        self.exec_function(sql, {'p_dogid': dogid, 'p_begdate': c_date, })

    def search_by_phone(self, phone_number, params):
        q = self.session.query(ApiClientResources)
        #q = q.join(ApiDogList)
        q = q.join(ApiClientProps, ApiClientProps.clsrv==ApiClientResources.id)
        q = q.filter(ApiClientProps.value==phone_number)
        q = q.filter(ApiClientResources.status!=4)
        q = q.filter(ApiClientProps.property==params['property'])
        q = q.filter(ApiClientResources.gid==params['gid'])
        q = q.filter(ApiClientResources.service==params['service'])

        return q.all()

    def get_status(self, dogid, s_date=datetime.now(), e_date=None):
        q = self.session.query(
            ApiAuditDogList.status,
            ApiAuditDogList.status_date
        )
        q = q.filter(ApiAuditDogList.dogid == dogid)
        if e_date:
            q = q.filter(ApiAuditDogList.status_date.between(s_date, e_date))
        else:
            q = q.filter(ApiAuditDogList.status_date <= s_date)

        q = q.order_by(desc(ApiAuditDogList.status_date))
        status = (q.first())
        if status:
            return {
                'status': status[0],
                'status_date': status[1],
            }
        else:
            return None

    def open_period(self, dogid, l_date):
        #if self.session
        self.exec_function('''
            begin
                o_mdb.api_close_billing_date.set_dog(:pdogid, :pdate);
                commit;
            end;
        ''',
        {
            'pdogid': dogid,
            'pdate': l_date,
        })

    def close_period(self, dogid):
        self.exec_function('''
            begin
                o_mdb.api_close_billing_date.clear_dog(:pdogid);
                commit;
            end;
        ''',
        {
            'pdogid': dogid,
        })

    def get_add_dog_attrib(self, dogid, attrid, cdate=datetime.now()):
        try:
            sql = '''
                select api_func.get_add_dog_attrib(:pdogid, :pattr, :pdate) address from dual
            '''
            params = {
                'pdogid': dogid,
                'pattr': attrid,
                'pdate': cdate,
            }
            return self.exec_function(sql, params)
        except:
            #return self.session.execute(self.error_sql)
            pass

    def get_vdog(self, dogid):
        vdogs = self.get_add_dog_attrib(dogid, 364)
        vdog = 'Интернет'
        if vdogs:
            for row in vdogs:
                if row[0]:
                    if type(row[0]) == unicode:
                        vdog = row[0].encode('utf-8')
                    elif type(row[0]) == str:
                        vdog = row[0]
                    else:
                        vdog = 'None'

        return vdog

    def get_dog_info(self, params={}):
        sql = '''
            select
                adl.dogid
                , adl.dogcode
                , nvl(api_func.get_add_dog_attrib(adl.dogid, 364, sysdate), 'Интернет') vdog
                , decode(adl.utid, 25, api_func.get_add_dog_attrib(adl.dogid, 291, sysdate), 26, api_func.get_add_dog_attrib(adl.dogid, 12, sysdate)) client
                , api_func.get_add_dog_attrib(adl.dogid, 292, sysdate) address
                , decode(adl.utid, 25, 'ФЛ', 26, 'ФЛ') ctype
                , adl.utid
                , adl.status
                , adl.startdate
                , adl.bill
            from api_dog_list adl
            --right outer join UAPI_V_QUERY_17441  vq on vq.f1 = adl.dogid
            where
                1 = 1
                %(params)s
        '''.decode('utf-8')
        param_str = ''
        param_data = {}
        if len(params) > 0:
            param_str, param_data = self.fill_params(params)
        nsql = sql % ({
            'params': param_str,
        })
        sparams = {}
        sparams.update(param_data)

        return self.session.execute(nsql, sparams)

    def get_v_query_details(self, dogid, params):
        q = self.session.query(V_Q_DETAILS)
        q = q.filter(V_Q_DETAILS.f10==dogid)
        q = self.get_parametrized_filter(V_Q_DETAILS, q, params)
        return q.all()
