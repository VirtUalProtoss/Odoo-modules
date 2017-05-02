# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class CONTRACTOR_T(Base):

    __tablename__ = 'CONTRACTOR_T'

    contractor_id = Column(Integer, primary_key=True)
    contractor = Column(String)

    def __repr__(self):

        return ('[%d]%s' % (
            self.contractor_id,
            self.contractor,
        )).encode('utf-8')
