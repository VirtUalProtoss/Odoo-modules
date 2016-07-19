# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .contractor_t import CONTRACTOR_T


class SWITCH_T(Base):

    __tablename__ = 'SWITCH_T'

    switch_id = Column(Integer, primary_key=True)
    switch_name = Column(String(200))
    switch_code = Column(String(20))
    switch_type = Column(String(200))
    contractor_id = Column(Integer, ForeignKey("CONTRACTOR_T.contractor_id"))
    network_id = Column(Integer)

    contractor = relation(CONTRACTOR_T, primaryjoin=(contractor_id == CONTRACTOR_T.contractor_id))

    def __repr__(self):

        return ('[%d]%s (%s:%s)' % (
            self.switch_id,
            self.switch_name,
            self.switch_type,
            self.switch_code,
        )).encode('utf-8')
