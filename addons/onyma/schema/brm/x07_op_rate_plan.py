# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .rateplan_t import RATEPLAN_T


class X07_OP_RATE_PLAN(Base):

    __tablename__ = 'X07_OP_RATE_PLAN'

    op_rate_plan_id = Column(Integer, primary_key=True)
    rateplan_id = Column(Integer, ForeignKey("RATEPLAN_T.rateplan_id"))
    op_rate_plan_type = Column(Integer)
    tarif_vol_type = Column(Integer)
    flag_garant_vol = Column(Integer)
    round_v_id = Column(Integer, ForeignKey("X07_ROUND_V.round_v_id"))

    rateplan_t = relation(RATEPLAN_T, primaryjoin=(rateplan_id==RATEPLAN_T.rateplan_id))


    def __repr__(self):

        return ('[%d][%d][%d][%d][%d][%d]' % (
            self.op_rate_plan_id,
            self.rateplan_id,
            self.op_rate_plan_type,
            self.tarif_vol_type,
            self.flag_garant_vol,
            self.round_v_id,
        )).encode('utf-8')
