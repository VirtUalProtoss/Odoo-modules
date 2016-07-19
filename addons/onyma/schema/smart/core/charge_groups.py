# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from datetime import date
from .accounts import Accounts

service_types = {
    6: 'Платеж',
    11: 'Перерасчет',
    601: 'АП',
}

class ChargeGroups(Base):
    __tablename__ = 'charge_groups'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(BigInteger, primary_key=True)
    top_account_id = Column(BigInteger, ForeignKey("core.accounts.id"))
    price_without_vat = Column(Numeric(17,6))
    quantity_type = Column(BigInteger)

    name = Column(String)


    pay_date = Column(DateTime)
    rate_date = Column(DateTime)
    charge_date = Column(DateTime)

    tariff_type = Column(Integer)
    service_type = Column(Integer)
    service_sub_type = Column(Integer)
    status = Column(Integer)
    total_with_vat = Column(Float)
    charge_class = Column(BigInteger)
    amount = Column(Float)
    without_vat = Column(Boolean)

    account = relationship(Accounts, primaryjoin=(top_account_id == Accounts.id))

    def __repr__(self):
        return ('[%s] %s [%d]%s %s %s' % (
            self.account.account_number,
            self.charge_date.strftime('%d.%m.%Y'),
            self.service_type,
            self.name,
            str(self.amount),
            str(self.total_with_vat),
        )).encode('utf-8')
