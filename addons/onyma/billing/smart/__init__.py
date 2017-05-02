# -*- coding: utf-8 -*-

__author__ = 'virtual'

from .. import Billing
from schema.smart.core.accounts import Accounts
from schema.smart.core.account_statuses import AccountStatuses
from schema.smart.core.tariffhistory import TariffHistory

from sqlalchemy import desc, asc

from datetime import datetime

statuses = {
    None: {'name': 'None', },
    -1: { 'name': 'unknown', },
    0: { 'name': 'Новый',},
    1: { 'name': '',},
    2: { 'name': '',},
    3: { 'name': 'Активный', },
    4: { 'name': '',},
    5: { 'name': 'Заблокированный', },
    6: { 'name': 'Удаленный', },
    7: { 'name': 'Закрытый', },
    8: { 'name': '', },
}


class Smart(Billing):

    def __init__(self, session):
        Billing.__init__(self, session)

    def get_bill(self, lschet):
        return self.get_table_data(Accounts, {'account_number': lschet,})

    def get_status(self, account, s_date=datetime.now()):
        status = self.get_table_data(AccountStatuses, {
            'account_id': account.id,
            'start_date': { 'check_type': '<=', 'value': s_date, },
            #'end_date': { 'check_type': '<=', 'value': s_date, },
        })
        return status

    def get_tariff(self, account, c_date=None, params={}):
        q = self.session.query(TariffHistory)
        if c_date:
            q = q.filter(TariffHistory.start_date>=c_date)
        q = q.filter(TariffHistory.account_id==account.id)
        q = self.get_parametrized_filter(TariffHistory, q, params)
        return q.all()

    def get_status_on_date(self, account, s_date=datetime.now(), e_date=None):
        q = self.session.query(AccountStatuses)
        q = q.filter(AccountStatuses.account_id==account.id)
        if e_date:
            q = q.filter(AccountStatuses.start_date>=s_date)
            q = q.filter(AccountStatuses.end_date<=e_date)
        else:
            q = q.filter(AccountStatuses.start_date<=s_date)
            #q = q.filter(AccountStatuses.end_date=None)
        q = q.order_by(desc(AccountStatuses.start_date))
        status = q.first()
        return status

    def get_accounts(self, params):
        q = self.session.query(Accounts)
        q = self.get_parametrized_filter(Accounts, q, params)
        return q.all()
