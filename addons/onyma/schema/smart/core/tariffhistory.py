# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .accounts import Accounts
from .tariffs import Tariffs


class TariffHistory(Base):
    __tablename__ = 'tariff_history'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("core.accounts.id"))
    tariff_id = Column(Integer, ForeignKey("core.tariffs.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    account = relation(Accounts, primaryjoin=(account_id == Accounts.id))
    tariff = relation(Tariffs, primaryjoin=(tariff_id == Tariffs.id))

    def __repr__(self):
        account = self.account
        tariff = self.tariff.name.encode('utf-8')
        return ("[%d]%s %s" % (self.id, account, tariff, ))
