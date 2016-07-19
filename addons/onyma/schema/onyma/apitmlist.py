# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiTmList(Base):

    __tablename__ = 'api_tm_list'

    tmid = Column(Integer, primary_key=True)
    tmname = Column(String)

    def __repr__(self):
        return ('[%d]' % (self.tmid, )).encode('utf-8')
