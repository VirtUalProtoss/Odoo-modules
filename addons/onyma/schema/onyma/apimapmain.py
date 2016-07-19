# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiMapMain(Base):

    __tablename__ = 'api_map_main'

    dmid = Column(Integer, primary_key=True)

    def __repr__(self):
        return ('[%d]' % (self.dmid, )).encode('utf-8')
