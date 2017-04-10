__author__ = 'virtual'

from ...schema import *
from ..onyma import *
from .apitrafdestd import ApiTrafDestD
from .apiclientresources import ApiClientResources


class MaskStat(Base):

    __tablename__ = 'mask_stat'

    mask = Column(String)
    mdate = Column(DateTime, primary_key=True)
    use1 = Column(Float)
    use2 = Column(Float)
    remark = Column(String)
    fid = Column(Integer)
    dmid = Column(Integer, ForeignKey("api_map_main.dmid"), primary_key=True)
    servid = Column(Integer, ForeignKey('api_services.servid'), primary_key=True)
    servdomid = Column(Integer) #, ForeignKey('api_domains.domainid'), primary_key=True)
    cost = Column(Float)
    tmid = Column(Integer, ForeignKey("api_tm_list.tmid"), primary_key=True)
    tdid = Column(Integer, ForeignKey("api_traf_dest_d.tdid"), primary_key=True)
    tdfid = Column(Integer) #, ForeignKey("api_traf_dest_d.tdid"), primary_key=True)
    rattr = Column(Integer)
    errorcode = Column(Integer)
    gid = Column(Integer) #ForeignKey("api_groups.gid")
    tdidbill = Column(Integer, ForeignKey("api_traf_dest_d.tdid"))
    usefact = Column(Float)
    asid = Column(Integer)
    pcost = Column(Float)
    edate = Column(Date)
    sesskey = Column(String(255))
    cdate = Column(Date)

    #amount = Column(Float)
    #comments = Column(String)
    #asid = Column(Integer)

    tpt = relation(ApiTrafDestD, primaryjoin=(tdid == ApiTrafDestD.tdid))
