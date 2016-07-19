# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class Tariffs(Base):
    __tablename__ = 'tariffs'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("core.groups.id"))
    service_type = Column(Integer)
    #service_sub_type = Column(Integer)
    name = Column(String)

    #account = relation(Accounts, primaryjoin=(account_id == Accounts.id))

    def __repr__(self):
        return ("[%d]%s" % (self.id, self.name, )).encode('utf-8')
