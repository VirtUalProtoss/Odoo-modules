# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .general_groups import GeneralGroups
#from .accounts import Accounts


class GeneralGrLinks(Base):
    __tablename__ = 'generalgr_links'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("core.general_groups.id"))
    account_id = Column(Integer, ForeignKey("core.accounts.id"))
    #service_type = Column(Integer)
    #service_sub_type = Column(Integer)

    #account = relation('Accounts', primaryjoin=(account_id == Accounts.id), foreign_keys=[account_id,])
    group = relation(GeneralGroups, primaryjoin=(group_id == GeneralGroups.id))

    def __repr__(self):
        return "[%d]"% (self.id, )
