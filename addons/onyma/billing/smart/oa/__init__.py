# -* coding: utf-8 -*-

__author__ = 'virtual'


from billing import Billing
from schema.smart.core.users import Users
from schema.smart.core.accounts import Accounts
from schema.smart.core.account_statuses import AccountStatuses

from sqlalchemy import desc, asc

from datetime import datetime


class OA(Billing):

    def __init__(self, session):
        Billing.__init__(self, session)

    def get_oa(self, params={}):
        return self.get_table_data(Users. params)

    def get_oa_statuses(self, oa):
        statuses = self.get_table_data(AccountStatuses, {
            'account_id': oa.account_id,
        })
        return statuses



    def get_oa_by_ls(self, lschet):
        q = self.session.query(Accounts)
        q = q.filter(Accounts.account_number==lschet)
        accounts = q.all()

        oas = []
        if accounts:
            for account in accounts:
                oq = self.session.query(Accounts)
                oq = oq.filter(Accounts.parent_id==account.id)
                oa_list = oq.all()
                if oa_list:
                    for oa in oa_list:
                        oas.append(oa)

        return oas

    def get_oa_status_on_date(self, oa, s_date=datetime.now(), e_date=None):
        q = self.session.query(AccountStatuses)
        q = q.filter(AccountStatuses.account_id==oa.account_id)
        if e_date:
            q = q.filter(AccountStatuses.start_date>=s_date)
            q = q.filter(AccountStatuses.end_date<=e_date)
        else:
            q = q.filter(AccountStatuses.start_date<=s_date)
            #q = q.filter(AccountStatuses.end_date=None)
        q = q.order_by(desc(AccountStatuses.start_date))
        status = q.first()
        return status

    def get_oa_statuses_on_date(self, oa, s_date=datetime.now(), e_date=None):
        q = self.session.query(AccountStatuses)
        q = q.filter(AccountStatuses.account_id==oa.account_id)
        q = q.filter(AccountStatuses.start_date>=s_date)
        q = q.order_by(asc(AccountStatuses.start_date))
        return q.all()

    def get_account_user(self, account):
        return self.get_table_data(Users, {'account_id' : account.id, })
