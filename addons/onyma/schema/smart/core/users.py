# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
#from .accounts import Accounts
from ..phone.users import Users as PhoneUsers


class Users(Base):
    __tablename__ = 'users'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("core.accounts.id"))
    service_type = Column(Integer)
    service_sub_type = Column(Integer)

    account = relation('Accounts', foreign_keys=[account_id,])
    phone = relationship(PhoneUsers, remote_side=PhoneUsers.user_id, backref='user')

    def __repr__(self):
        return "%d:%d:%d:%d"% (self.id, self.account_id, self.service_type, self.service_sub_type, )
