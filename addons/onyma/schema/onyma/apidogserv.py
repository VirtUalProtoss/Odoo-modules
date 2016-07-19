# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *
from ...schema.onyma import *
from .apitmlist import ApiTmList


class ApiDogServ(Base):

    __tablename__ = 'api_dog_serv_f'

    dmid = Column(Integer, ForeignKey("api_map_main.dmid"), primary_key=True)
    begdate = Column(Date)
    enddate = Column(Date)
    cost = Column(Float)
    base_cost = Column(Float)
    remark = Column(String(250))
    clsrv = Column(String(4000))
    clsrvid = Column(Integer)
    servid = Column(Integer, ForeignKey("api_services.servid"), primary_key=True)
    tmid = Column(Integer, ForeignKey("api_tm_list.tmid"), primary_key=True)
    cntr = Column(Integer) # Коэффициент
    tdid = Column(Integer, ForeignKey("api_traf_dest.tdid"))
    serv_alias = Column(String(4000))
    operid_start = Column(Integer)
    operid_stop = Column(Integer)
    last_date = Column(Date)
    next_date = Column(Date)
    ccntr = Column(Integer) # Ценовой коэффициент

    tp = relation(ApiTmList, primaryjoin=(tmid == ApiTmList.tmid))

    '''
    def __repr__(self):
        row_str = '[%d]%s %f %f %s %s' % (
            self.clsrvid,
            self.clsrv,
            self.base_cost,
            self.cost,
            self.begdate,
            self.enddate,
        )
        return row_str.encode('utf-8')
    '''
