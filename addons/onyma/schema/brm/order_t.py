# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class ORDER_T(Base):

    __tablename__ = 'ORDER_T'

    rateplan_id = Column(Integer, primary_key=True)
    rateplan_name = Column(String(200))
    ratesystem_id = Column(Integer)
    note = Column(String(200))
    rateplan_code = Column(String(255))
    service_id = Column(Integer)
    subservice_id = Column(Integer)
    tax_incl = Column(String(1))
    currency_id = Column(Integer)
    agent_percent = Column(Integer)
    rateplan_type = Column(String(10))

    def __repr__(self):

        return ('[%d][%s][%s][%s](%s-%s) %s' % (
            self.rateplan_id,
            str(self.ratesystem_id),
            str(self.service_id),
            str(self.subservice_id),
            self.rateplan_type,
            self.rateplan_code,
            self.rateplan_name,
        )).encode('utf-8')
