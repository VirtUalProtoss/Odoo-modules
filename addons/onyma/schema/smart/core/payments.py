# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from ..core.accounts import Accounts
from ..core.users import Users
from ..acct.payments import Payments as AcctPayments

payment_types = {
    1: {
        None: { 'onyma_name': 'Платежи (касса)', 'smart_name': 'Наличный', 'onyma_id': -9, },
    },
    2: {
        None: { 'onyma_name': 'Платежи (б/н)', 'smart_name': 'Безналичный', 'onyma_id': -1, },
    },
    10: {
        6: { 'onyma_name': 'Платежи (ТТК)', 'smart_name': 'Онлайн платёж ТТК', 'onyma_id': -103, },
        8: { 'onyma_name': 'Платежи (б/н)', 'smart_name': 'Безналичный платеж КТТК', 'onyma_id': -1, },
        2: { 'onyma_name': 'Перевод средств на другой ЛС', 'smart_name': 'Перенос средств', 'onyma_id': 56, },
    },
}


class Payments(Base):
    __tablename__ = 'payments'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    acct_pid = Column(String, ForeignKey('acct.payments.id'))
    #provider_company_id = Column(Integer)
    payment_date = Column(DateTime)
    #amount_rur = Column(Float)
    tx_id = Column(Integer)
    type = Column(Integer)

    #loaded = Column(Integer)
    status = Column(Integer)
    #error = Column(String)
    description = Column(String)
    paymenttype_id = Column(Integer, ForeignKey('core.payment_types.id'))
    operator_name = Column(String)
    #charge_class = Column(Integer)
    create_date = Column(DateTime)
    extract_date = Column(DateTime)
    #service_type = Column(Integer)
    #service_sub_type = Column(Integer)

    #account = relation(Accounts, primaryjoin=(account_num == Accounts.account_number))
    #account = relationship(Accounts, primaryjoin=(account_num == Accounts.account_number)) #, remote_side='account_number', backref='payments')
    #payment_type = relation(PaymentTypes, primaryjoin=(paymenttype_id == PaymentTypes.id))
    acct_payment = relation(AcctPayments, primaryjoin=(acct_pid == AcctPayments.id), backref='cpayment')
    #operator = relation(Users, primaryjoin=(operator_name == Users.))


    def __repr__(self):

        return ('[%s:%s] %s' % (
            self.operator_name,
            self.type,
            self.payment_date.strftime('%d.%m.%Y'),
        )).encode('utf-8')
