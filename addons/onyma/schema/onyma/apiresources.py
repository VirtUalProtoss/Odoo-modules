# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiResources(Base):

    __tablename__ = 'api_resources'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    srvname = Column(String)

    def __repr__(self):
        return ('[%d]' % (self.id, )).encode('utf-8')
