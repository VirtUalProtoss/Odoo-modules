# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class PaymentTypes(Base):
    __tablename__ = 'payment_types'

    __table_args__ = {'extend_existing': True, 'schema':'acct', }

    id = Column(Integer, primary_key=True)
    core_id = Column(Integer) #, ForeignKey("core.accounts.id"))
    status = Column(Integer)
    subtype = Column(Integer)
    name = Column(String)
    comments = Column(String)

    #account = relation(Accounts, primaryjoin=(account_id == Accounts.id))

    def __repr__(self):
        return "[%d]:%s"% (self.id, self.name, )
