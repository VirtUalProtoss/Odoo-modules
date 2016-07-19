# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from ..core.users import Users as CUsers
from ..core.accounts import Accounts

class Operators(Base):
    __tablename__ = 'operators'

    __table_args__ = {'extend_existing': True, 'schema':'phone', }

    id = Column(Integer, primary_key=True)
    name = Column(String)
    provider_account_id = Column(Integer, ForeignKey('core.accounts.id'))
    client_account_id = Column(Integer, ForeignKey('core.accounts.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    islocal = Column(Boolean, nullable=None)
    iszone = Column(Boolean, nullable=None)
    isdistant = Column(Boolean, nullable=None)
    description = Column(String)
    isbase = Column(Boolean, nullable=None)
    shift = Column(Integer, nullable=None)

    provider = relation(Accounts, primaryjoin=(provider_account_id == Accounts.id))
    client = relation(Accounts, primaryjoin=(client_account_id == Accounts.id))


    def __repr__(self):
        return ('[%d]%s (%s-%s)' % (self.id, self.name, self.provider, self.client, )).encode('utf-8')
