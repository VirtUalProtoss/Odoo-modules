# -*- coding: utf-8 -*-

__author__ = 'virtual'

from .. import Billing
from schema.onyma.apicosts import ApiCosts
from schema.onyma.apitrafdestd import ApiTrafDestD


class Costs(Billing):

    def __init__(self, session):
        Billing.__init__(self, session)

    def insert_cost(self, cost):
        sql = '''
            begin
                o_mdb.api_tariff.ins_costs(
                    pdomid => :domainid,
                    ptmid => :tmid,
                    pservid => :servid,
                    pdaytype => :daytype,
                    pstart_date => :start_date,
                    pstop_date => :stop_date,
                    ptstart => :tstart,
                    ptend => :tend,
                    pcost => :cost,
                    pmask => :mask,
                    ptdid => :tdid,
                    pround0 => :round0,
                    pround1 => :round1,
                    proundn => :roundn,
                    soperid => :soperid,
                    eoperid => null,
                    pmspid => null
                );
                commit;
            --exception
            --    when others then rollback;
            end;
        '''
        params = cost
        try:
            self.exec_function(sql, params)
        except:
            self.get_error_message()

    def update_cost(self, cost):
        sql = '''
            begin
                o_mdb.api_tariff.upd_costs(
                    pdomid => :domainid,
                    ptmid => :tmid,
                    pservid => :servid,
                    pdaytype => :daytype,
                    pstart_date => :start_date,
                    pstop_date => :stop_date,
                    ptstart => :tstart,
                    ptend => :tend,
                    pcost => :cost,
                    pmask => :mask,
                    ptdid => :tdid,
                    pround0 => :round0,
                    pround1 => :round1,
                    proundn => :roundn,
                    soperid => :soperid,
                    eoperid => null,
                    pmspid => null
                );
                commit;
            --exception
            --    when others then rollback;
            end;
        '''
        params = cost
        try:
            self.exec_function(sql, params)
        except:
            self.get_error_message()

    def get_tdid_by_tdval(self, tdval, params={}):
        q = self.session.query(ApiTrafDestD)
        q = q.filter(ApiTrafDestD.tdval==tdval)
        q = self.get_parametrized_filter(ApiTrafDestD, q, params)
        return q.all()

    def get_tpt_by_tdid(self, tdid, params={}):
        q = self.session.query(ApiTrafDestD)
        q = q.filter(ApiTrafDestD.tdid==tdid)
        q = self.get_parametrized_filter(ApiTrafDestD, q, params)
        return q.one()

    def get_costs(self, params={}):
        q = self.session.query(ApiCosts)
        q = self.get_parametrized_filter(ApiCosts, q, params)
        return q.all()
