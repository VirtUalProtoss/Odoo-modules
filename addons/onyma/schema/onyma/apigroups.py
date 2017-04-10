# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiGroups(Base):

    __tablename__ = 'api_groups'

    __table_args__ = {'extend_existing': True, }

    gid = Column(Integer, primary_key=True)
    gidup = Column(Integer, ForeignKey("api_groups.gid"))
    g_name = Column(String(4000))
    domainid = Column(Integer)

    def __repr__(self):
        return ('[%d]%s' % (self.id, self.g_name, )).encode('utf-8')
