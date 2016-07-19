# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .switch_t import SWITCH_T
from .x07_op_rate_plan import X07_OP_RATE_PLAN
from .x07_srv_dct import X07_SRV_DCT

class X07_ORD_SERVICE_D_T(Base):

    __tablename__ = 'X07_ORD_SERVICE_D_T'

    rec_id = Column(Integer, primary_key=True)
    op_rate_plan_id = Column(Integer, ForeignKey("X07_OP_RATE_PLAN.op_rate_plan_id"))
    phone_from = Column(String(20))
    phone_to = Column(String(20))
    switch_id = Column(Integer, ForeignKey("SWITCH_T.switch_id"))
    srv_id = Column(Integer, ForeignKey("X07_SRV_DCT.srv_id"))
    date_from = Column(Date)
    date_to = Column(Date)
    notes = Column(String(256))

    switch = relation(SWITCH_T, primaryjoin=(switch_id == SWITCH_T.switch_id))
    op_rate_plan = relation(X07_OP_RATE_PLAN, primaryjoin=(op_rate_plan_id == X07_OP_RATE_PLAN.op_rate_plan_id))
    service = relation(X07_SRV_DCT, primaryjoin=(srv_id == X07_SRV_DCT.srv_id))

    def date_to_str(self, date_value):
        if date_value:
            return date_value.strftime('%Y-%m-%d %H:%M')
        else:
            return ' --- '

    def __repr__(self):

        return '[%d][%d][%d]%d: %s-%s (%s - %s)' % (
            self.op_rate_plan_id,
            self.rec_id,
            self.switch_id,
            self.srv_id,
            self.phone_from,
            self.phone_to,
            self.date_to_str(self.date_from),
            self.date_to_str(self.date_to),
        )
