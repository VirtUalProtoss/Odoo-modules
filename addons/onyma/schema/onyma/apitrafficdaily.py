__author__ = 'virtual'

from ...schema import *
from ..onyma import *
from .apitrafdestd import ApiTrafDestD
from .apiclientresources import ApiClientResources


class ApiTrafficDaily(Base):

    __tablename__ = 'api_traffic_daily'

    dmid = Column(Integer, ForeignKey("api_map_main.dmid"), primary_key=True)
    usedate = Column(DateTime, primary_key=True)
    servid = Column(Integer, ForeignKey('api_services.servid'), primary_key=True)
    useserv = Column(Float)
    res = Column(Integer, ForeignKey("api_client_resources.id"), primary_key=True)
    useserv1 = Column(Float)
    usefact = Column(Float)
    cost = Column(Float)
    amount = Column(Float)
    tmid = Column(Integer, ForeignKey("api_tm_list.tmid"), primary_key=True)
    tdid = Column(Integer, ForeignKey("api_traf_dest_d.tdid"), primary_key=True)
    tdidbill = Column(Integer, ForeignKey("api_traf_dest_d.tdid"))
    remark = Column(String)
    spres = Column(Integer, ForeignKey("api_client_resources.id"))
    mask = Column(String)
    gid = Column(Integer) #ForeignKey("api_groups.gid")
    comments = Column(String)
    fid = Column(Integer)
    tdfid = Column(Integer)
    pcost = Column(Float)
    asid = Column(Integer)

    tpt = relation(ApiTrafDestD, primaryjoin=(tdid == ApiTrafDestD.tdid))
    clsrv = relationship(ApiClientResources, foreign_keys=[res,], backref='traffic')
