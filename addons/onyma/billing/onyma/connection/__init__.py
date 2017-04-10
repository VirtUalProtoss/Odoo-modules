# -*- coding: utf-8 -*-

__author__ = 'virtual'

from .. import Onyma
from sqlalchemy import desc
from datetime import datetime
from schema.onyma.apiclientresources import ApiClientResources
from schema.onyma.apiresources import ApiResources
from schema.onyma.apiclientprops import ApiClientProps
from schema.onyma.apiclsrvstatushistory import ApiClsrvStatusHistory
from schema.onyma.apidogserv import ApiDogServ
from schema.onyma.apitrafficdaily import ApiTrafficDaily
from schema.onyma.apitrafdestd import ApiTrafDestD
from schema.onyma.apimaskstat import ApiMaskStat
from schema.onyma.apicosts import ApiCosts
from schema.onyma.apitmlist import ApiTmList
from schema.onyma.maskstat import MaskStat

from sqlalchemy import Table
import sqlalchemy.types as types

class TR_PROPS_W_TYPE(types.UserDefinedType):

    property = None
    value = None
    value_type = None
    value_num = None

    def __init__(self, property, value, value_type='V', num=0):
        types.UserDefinedType.__init__(self)
        self.property = property
        self.value = value
        self.value_type = value_type
        self.value_num = num

    def get_col_spec(self):
        return "TR_PROPS_W_TYPE(%d, '%s', '%s', %d)" % (
            self.property,
            self.value,
            self.value_type,
            self.value_num,
        )

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process


class TT_PROPS_W_TYPE(types.UserDefinedType):

    properties = []

    def __init__(self):
        types.UserDefinedType.__init__(self)

tt_props = TT_PROPS_W_TYPE


class Connection(Onyma):

    error_sql = '''
        select err.get_error_message from dual
    '''

    def __init__(self, session):
        Onyma.__init__(self, session)

    def set_status(self, clsrv, status, s_date=datetime.now()):
        try:
            self.exec_function('''
                begin
                    o_mdb.api_change_connection.set_status(:pclsrv, :pstatus, :pdate);
                    commit;
                exception
                    when others then rollback;
                end;
            ''',
            {
                'pstatus': status,
                'pdate': s_date,
                'pclsrv': clsrv,
            })
            return self.session.execute(self.error_sql)
        except:
            return self.session.execute(self.error_sql)

    def get_status(self, clsrv, s_date=datetime.now(), e_date=None):
        q = self.session.query(ApiClsrvStatusHistory)
        q = q.filter(ApiClsrvStatusHistory.sid == clsrv)
        if e_date:
            q = q.filter(ApiClsrvStatusHistory.sdate.between(s_date, e_date))
        else:
            q = q.filter(ApiClsrvStatusHistory.sdate <= s_date)

        q = q.order_by(desc(ApiClsrvStatusHistory.sdate))
        return q.first()

    def get_statuses(self, clsrv, s_date=datetime.now(), e_date=None):
        q = self.session.query(ApiClsrvStatusHistory)
        q = q.filter(ApiClsrvStatusHistory.sid == clsrv)
        if e_date:
            q = q.filter(ApiClsrvStatusHistory.sdate.between(s_date, e_date))
        else:
            q = q.filter(ApiClsrvStatusHistory.sdate <= s_date)

        q = q.order_by(ApiClsrvStatusHistory.sdate)
        return q.all()

    def get_connection_by_property_value(self, connections, property, value):
        q_conn = self.session.query(ApiClientProps)
        q_conn = q_conn.join(ApiClientResources, aliased=True)

        if len(connections) > 0:
            conns = []
            for conn in connections:
                conns.append(conn.id)
            q_conn = q_conn.filter(ApiClientResources.id.in_(conns))
        else:
            return None
        q_conn = q_conn.filter(ApiClientProps.property==property)
        q_conn = q_conn.filter(ApiClientProps.value==value)
        #print q_conn
        return q_conn.all()

    def get_connections_by_property(self, property, params={}):
        q = self.session.query(ApiClientProps)

        q = q.filter(ApiClientProps.property==property)
        q = self.get_parametrized_filter(ApiClientProps, q, params)
        props = q.all()
        clsrv_list = []
        for prop in props:
            clsrv_list.append(prop.clsrv)

        params.update({
            'id': {'check_type': 'in', 'value': clsrv_list, }
        })
        q = self.session.query(ApiClientResources)
        q = self.get_parametrized_filter(ApiClientResources, q, params)
        return q.all()

    def set_tariff(self, clsrv, tmid, start_date):
        sql = '''
            begin
                o_mdb.api_change_connection.set_tmid(:pclsrv, :ptmid, :pstart_date);
                commit;
            exception
                when others then rollback;
            end;
        '''
        self.exec_function(sql, {
            'pclsrv': clsrv,
            'ptmid': tmid,
            'pstart_date': start_date,
        })

    def fill_property(self, property, value, value_type, num):
        return 'o_mdb.' + str(TR_PROPS_W_TYPE(property, value, value_type, num))

    def fill_properties(self, props):
        return 'o_mdb.TT_PROPS_W_TYPE(' + ','.join(props) + ')'

    def get_properties_by_connection(self, connid, params={}):
        q = self.session.query(ApiClientProps)
        q = q.filter(ApiClientProps.clsrv==connid)
        q = self.get_parametrized_filter(ApiClientProps, q, params)
        return q.all()

    def set_prop_val(self, clsrv, pprop):
        upd_sql = '''
            begin
                o_mdb.api_change_connection.upd_property_value(:p_clsrv, :p_prop);
                commit;
            exception
                when others then rollback;
            end;
        '''
        self.exec_function(upd_sql, {
            'p_clsrv': clsrv,
            'p_prop': pprop,
        })

    def set_property_value(self, clsrv, property, value, value_type='V', real_value=None, parentclsrv=None):
        sql = '''
            declare
                    tt_prop o_mdb.TT_PROPS_W_TYPE;
                    tr_prop o_mdb.TR_PROPS_W_TYPE;
            begin
                tr_prop := o_mdb.TR_PROPS_W_TYPE(%d, '%s', '%s', %d);
                tt_prop := o_mdb.TT_PROPS_W_TYPE(tr_prop);

                o_mdb.api_change_connection.upd_property_value(
                    p_clsrv => :clsrv,
                    p_prop => tt_prop
                );
                commit;
            end;
        ''' % (property, value, value_type, 0, )
        self.exec_function(sql, {'clsrv': clsrv, })

    def set_connection_notes(self, clsrv, value):
        sql = '''
            begin
                o_mdb.api_change_connection.set_notes(
                    :pclsrv,
                    :pnotes
                );
                commit;
            end;
        '''
        self.exec_function(sql, {'pclsrv': clsrv, 'pnotes': value, })

    def get_connection_by_value(self, dogid, property, value, params={}):
        q_conn = self.session.query(ApiClientResources)
        q_conn = q_conn.join(ApiClientProps)
        q_conn = q_conn.filter(ApiClientResources.dogid==dogid)
        q_conn = q_conn.filter(ApiClientProps.property==property)
        q_conn = q_conn.filter(ApiClientProps.value==value)
        return q_conn.all()

    def get_connection_by_phone_number(self, number, property, params={}):
        q = self.session.query(ApiClientResources)
        q = q.join(ApiClientProps)
        q = q.filter(ApiClientProps.property==property)
        q = q.filter(ApiClientProps.value==number)
        q = self.get_parametrized_filter(ApiClientProps, q, params)
        return q.all()

    def get_connections_by_dogid_res(self, dogid, resource, params={}):
        q_conn = self.session.query(ApiClientResources)
        q_conn = q_conn.filter(ApiClientResources.dogid==dogid)
        q_conn = q_conn.filter(ApiClientResources.service==resource)
        if len(params) > 0:
            q_conn = self.get_parametrized_filter(ApiClientResources, q_conn, params)
        return q_conn.all()

    def get_connections_info(self, dogid, params={}):
        q_conn = self.session.query(
            ApiClientResources.id,
            ApiClientResources.service,
            ApiClientResources.name,
            ApiClientResources.notes,
            ApiClientResources.startdate,
            ApiClientResources.status,
            ApiDogServ.base_cost,
            ApiDogServ.cost,
            ApiTmList.tmname,
            ApiResources.srvname
        )
        q_conn = q_conn.join(ApiDogServ, ApiClientResources.id==ApiDogServ.clsrvid)
        q_conn = q_conn.join(ApiTmList, ApiTmList.tmid==ApiDogServ.tmid)
        q_conn = q_conn.join(ApiResources, ApiResources.id==ApiClientResources.service)
        q_conn = q_conn.filter(ApiClientResources.dogid==dogid)
        q_conn = q_conn.filter(ApiDogServ.enddate==None)
        if len(params) > 0:
            q_conn = self.get_parametrized_filter(ApiClientResources, q_conn, params)
        return q_conn.all()

    def get_connections_by_dogid(self, dogid, params={}):
        q_conn = self.session.query(ApiClientResources)
        q_conn = q_conn.filter(ApiClientResources.dogid==dogid)
        if len(params) > 0:
            q_conn = self.get_parametrized_filter(ApiClientResources, q_conn, params)
        return q_conn.all()

    def get_tariff(self, clsrv, servid=None):
        q = self.session.query(ApiDogServ)
        q = q.filter(ApiDogServ.clsrvid==clsrv)
        if servid:
            q = q.filter(ApiDogServ.servid==servid)
        return q.all()

    def get_calls(self, params):
        q = self.session.query(ApiTrafficDaily)
        q = q.join(ApiTrafDestD, ApiTrafficDaily.tdid==ApiTrafDestD.tdid)
        q = q.join(ApiClientResources, ApiClientResources.id==ApiTrafficDaily.res)
        q = self.get_parametrized_filter(ApiTrafficDaily, q, params)
        return q.all()

    def get_tpt(self, params):
        q = self.session.query(ApiTrafDestD)
        q = self.get_parametrized_filter(ApiTrafDestD, q, params)
        return q.all()

    def get_mask_stat(self, params):
        q = self.session.query(ApiMaskStat)
        q = self.get_parametrized_filter(ApiMaskStat, q, params)
        return q.all()

    def update_mask_tdid(self, uparams, wparams):
        mstat = MaskStat()
        for wparam in wparams:
            if wparam in mstat.__dict__:
                mstat.__dict__[wparam] = wparams[wparam]

    def set_personal_tariff(self, clsrv, servid, cost=None, c_date=datetime.now(), params={}):
        sql = '''
            begin
            o_mdb.api_change_connection.add_personal_tariff(
                p_clsrv => :p_clsrv,
                p_servid => :p_servid,
                p_cost => :p_cost,
                p_begin_date => :p_begin_date,
                p_end_date => :p_end_date,
                p_tdid => :p_tdid,
                p_coeff => :p_coeff,
                p_use_default_cost => :p_use_default_cost,
                p_serv_alias => :p_serv_alias,
                p_remark => :p_remark,
                p_no_mcost => :p_no_mcost,
                pccntr => :pccntr
            );
            commit;
            --rollback;
            end;
        '''
        pm = {
            #'p_clsrv': None,
            #'p_servid': None,
            'p_cost': None,
            'p_begin_date': None,
            'p_end_date': None,
            'p_remark': None,
            'p_coeff': None,
            'pccntr': 1,
            'p_serv_alias': None,
            'p_tdid': None,
            'p_use_default_cost': None,
            'p_no_mcost': None,
        }
        pm.update(params)
        pm.update({
            'p_clsrv': clsrv,
            'p_servid': servid,
            'p_cost': cost,
            'p_begin_date': c_date,
        })
        self.exec_function(sql, pm)

    def get_connections(self, resource_id, params={}):
        q = self.session.query(ApiClientResources)
        q = q.filter(ApiClientResources.service==resource_id)
        q = self.get_parametrized_filter(ApiClientResources, q, params)
        return q.all()

    def get_prop_connections(self, dogid, resource_id, params={}):
        q = self.session.query(ApiClientProps)
        q = q.join(ApiClientResources, ApiClientProps.clsrv==ApiClientResources.id)
        q = q.filter(ApiClientResources.service==resource_id)
        q = q.filter(ApiClientResources.dogid==dogid)
        q = self.get_parametrized_filter(ApiClientProps, q, params)
        return q.all()
