# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from ..core.accounts import Accounts
from payment_types import PaymentTypes
from ..core.users import Users


class Bills(Base):
    __tablename__ = 'bills'

    __table_args__ = {'extend_existing': True, 'schema':'acct', }

    id = Column(Integer, primary_key=True)
    num = Column(String)
    account_num = Column(String, ForeignKey('core.accounts.account_number'))
    provider_company_id = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    bill_date = Column(DateTime)
    create_date = Column(DateTime)
    pay_date = Column(DateTime)
    currency_code = Column(Integer)
    loaded = Column(Boolean)
    status = Column(Integer)
    account_group = Column(BigInteger)
    doc_num = Column(String)
    doc_date = Column(DateTime)

    #account = relation(Accounts, primaryjoin=(account_num == Accounts.account_number))
    account = relationship(Accounts, primaryjoin=(account_num == Accounts.account_number)) #, remote_side='account_number', backref='payments')
    #operator = relation(Users, primaryjoin=(operator_name == Users.))


    def __repr__(self):
        return "[%d:%s] %s %s" % (
            self.status,
            self.account_num,
            self.num,
            self.bill_date.strftime('%d.%m.%Y'),
        )
