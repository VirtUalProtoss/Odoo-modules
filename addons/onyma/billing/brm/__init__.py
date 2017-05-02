# -*- coding: utf-8 -*-

__author__ = 'virtual'

from billing import Billing
from schema.brm.x07_ord_service_d_t import X07_ORD_SERVICE_D_T as Ranges
from schema.brm.x07_op_rate_plan import X07_OP_RATE_PLAN as RatePlans
from schema.brm.bdr_oper_t import BDR_OPER_T as Calls


class Brm(Billing):

    or_sr_d_keys = []
    or_sr_d_last = 40000

    def __init__(self, session):
        Billing.__init__(self, session)

    def get_brm_ranges(self, params={}):
        q = self.session.query(Ranges)
        q = self.get_parametrized_filter(Ranges, q, params)
        ranges = q.all()
        #for range in ranges:
        #    print range, range.switch, range.switch.contractor, range.service, range.op_rate_plan.rateplan_t
        return ranges

    def find_next_free_pk(self, rec_id, rec_arr):
        pk_id = -1
        if rec_id not in rec_arr:
            pk_id = rec_id
        else:
            if rec_id == rec_arr[-1]:
                pk_id += rec_id + 1
            else:
                for id in rec_arr:
                    if id + 1 not in rec_arr:
                        pk_id = id + 1
                        break

        return pk_id

    def get_ord_svc_last_pk(self):
        if len(self.or_sr_d_keys) == 0:
            sql = '''
                select rec_id from X07_ORD_SERVICE_D_T where rec_id > %d order by rec_id asc
            ''' % (self.or_sr_d_last, )
            result = self.session.execute(sql)
            if result:
                for row in result:
                    self.or_sr_d_keys.append(row[0])

        self.or_sr_d_last = self.find_next_free_pk(self.or_sr_d_last, self.or_sr_d_keys)
        if self.or_sr_d_last not in self.or_sr_d_keys:
            if self.or_sr_d_last < len(self.or_sr_d_keys):
                self.or_sr_d_keys.insert(self.or_sr_d_last, self.or_sr_d_last)
            else:
                if self.or_sr_d_last > self.or_sr_d_keys[-1]:
                    self.or_sr_d_keys.append(self.or_sr_d_last)
                else:
                    self.or_sr_d_keys.insert(0, self.or_sr_d_last)
            self.or_sr_d_keys.sort()
        return self.or_sr_d_last

    def add_range_service(self, rp_id, switch_id, svc_id, range):
        rec_id = self.get_ord_svc_last_pk()
        if rec_id < 0:
            return None
        insert_sql = '''
            declare
                rec_id integer;
            begin
                rec_id := PK104_X7_TOPS.OrderService_D_Add(
                    %(id)d,
                    %(op_rate_plan_id)d,
                    %(dn_from)s,
                    %(dn_to)s,
                    %(switch_id)d,
                    %(subservice_id)d,
                    %(date_from)s,
                    %(date_to)s
                );
                commit;
            end;
        '''
        if range['date_from']:
            date_from = "to_date('" + range['date_from'].strftime('%Y-%m-%d') + "', 'yyyy-mm-dd')"
        else:
            date_from = 'null'

        if range['date_to']:
            date_to = "to_date('" + range['date_to'].strftime('%Y-%m-%d') + "', 'yyyy-mm-dd')"
        else:
            date_to = 'null'
        fields = {
            'id': rec_id,
            'op_rate_plan_id':  rp_id, # get from brm (hard map)
            'dn_from': range['phone_from'], # get from smart
            'dn_to': range['phone_to'], # get from smart
            'switch_id': switch_id, # 66
            'subservice_id': svc_id, # need get (hard map)
            'date_from': date_from, # get from sart
            'date_to': date_to, # get from smart
        }
        self.session.execute(insert_sql % (fields))

    def get_op_rp_id(self, rp_id, rp_type=1):
        return self.get_table_data(RatePlans, {'rateplan_id': rp_id, 'op_rate_plan_type': rp_type, })

    def check_range_exist(self, range, params={}):
        q = self.session.query(Ranges)
        q = self.get_parametrized_filter(Ranges, q, range)
        q = self.get_parametrized_filter(Ranges, q, params)
        cq = q.count()
        if cq > 0:
            result = q.one()
            if result:
                if result.rec_id:
                    return True

        return False

    def get_calls(self, params):
        q = self.session.query(Calls)
        q = self.get_parametrized_filter(Calls, q, params)
        return q.all()
