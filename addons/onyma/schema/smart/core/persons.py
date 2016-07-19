# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class Persons(Base):
    __tablename__ = 'persons'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    #account_id = Column(Integer, ForeignKey("core.accounts.id"))
    #service_type = Column(Integer)
    #service_sub_type = Column(Integer)

    #account = relation(Accounts, primaryjoin=(account_id == Accounts.id))

    def __repr__(self):
        return "[%d]"% (self.id, )