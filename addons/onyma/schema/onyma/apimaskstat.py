__author__ = 'virtual'

from ...schema import *
from ...schema.onyma import *
from .apitrafdestd import ApiTrafDestD
from .apiclientresources import ApiClientResources


class ApiMaskStat(Base):

    __tablename__ = 'api_mask_stat'

    mask = Column(String)
    mdate = Column(DateTime, primary_key=True)
    use1 = Column(Float)
    remark = Column(String)
    dmid = Column(Integer, ForeignKey("api_map_main.dmid"), primary_key=True)
    servid = Column(Integer, ForeignKey('api_services.servid'), primary_key=True)
    servdomid = Column(Integer) #, ForeignKey('api_domains.domainid'), primary_key=True)
    cost = Column(Float)
    tmid = Column(Integer, ForeignKey("api_tm_list.tmid"), primary_key=True)
    tdid = Column(Integer, ForeignKey("api_traf_dest_d.tdid"), primary_key=True)
    errorcode = Column(Integer)
    gid = Column(Integer) #ForeignKey("api_groups.gid")
    tdidbill = Column(Integer, ForeignKey("api_traf_dest_d.tdid"))
    use2 = Column(Float)
    usefact = Column(Float)
    pcost = Column(Float)
    fid = Column(Integer)
    tdfid = Column(Integer)
    res = Column(Integer, ForeignKey("api_client_resources.id"), primary_key=True)
    spres = Column(Integer, ForeignKey("api_client_resources.id"))

    #amount = Column(Float)
    #comments = Column(String)
    #asid = Column(Integer)

    tpt = relation(ApiTrafDestD, primaryjoin=(tdid == ApiTrafDestD.tdid))
    clsrv = relationship(ApiClientResources, foreign_keys=[res,], backref='mask_stat')
