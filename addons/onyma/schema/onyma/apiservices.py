# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiServices(Base):

    __tablename__ = 'api_services'

    servid = Column(Integer, primary_key=True)
    servname = Column(String)
    unitid = Column(Integer)

    def __repr__(self):
        return ('[%d]%s' % (self.id, self.servname, )).encode('utf-8')
