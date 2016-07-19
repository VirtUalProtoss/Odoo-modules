# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class BDR_OPER_T(Base):

    __tablename__ = 'bdr_oper_t'

    start_time = Column(DateTime)

    cdr_id = Column(Integer, primary_key=True)

    abn_a = Column(String(40))
    abn_b = Column(String(40))
    duration = Column(Integer)
    trf_type = Column(Integer)
    account_id = Column(Integer)
    order_id = Column(Integer)
    price_id = Column(Integer)
    bdr_status = Column(Integer)

    rep_period = Column(Date)

    bill_minutes = Column(Float)
    amount = Column(Float)
    tariff = Column(Float)
    bill_id = Column(Integer)
    item_id = Column(Integer)

    service_id = Column(Integer)
    subservice_id = Column(Integer)
    parent_subsrv_id = Column(Integer)
    order_swtg_id = Column(Integer)
    order_body_id = Column(Integer)
    bdr_type_id = Column(Integer)

    #tax_incl = Column(String(1))
    #currency_id = Column(Integer)
    #agent_percent = Column(Integer)
    #rateplan_type = Column(String(10))

    rateplan_id = Column(Integer)
    op_rate_plan_id = Column(Integer)
    trunk_group_in = Column(String(16))
    trunk_group_out = Column(String(16))


    '''
        START_TIME	DATE
        DURATION	NUMBER
        LOCAL_TIME	DATE
        UTC_OFFSET	INTERVAL DAY(0) TO SECOND(0)
        VOL_TYPE	NUMBER
        SAVE_DATE	DATE
        MODIFY_DATE	DATE
        ITEM_DATE	DATE
        SW_NAME	VARCHAR2(16 BYTE)
        PREF_B	VARCHAR2(16 BYTE)
        TERM_Z_NAME	VARCHAR2(256 BYTE)
    '''

    def __repr__(self):

        return ('[%d]%s %s:%s => %s:%s %s %s' % (
            self.cdr_id,
            self.start_time.strftime('%d.%m.%Y %H:%M:%S'),
            self.trunk_group_in,
            self.abn_a,
            self.trunk_group_out,
            self.abn_b,
            str(self.duration),
            str(self.tariff),
        )).encode('utf-8')
