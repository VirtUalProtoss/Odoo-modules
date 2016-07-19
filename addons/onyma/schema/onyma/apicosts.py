__author__ = 'virtual'

from ...schema import *
from ...schema.onyma import *


class ApiCosts(Base):

    __tablename__ = 'api_costs'

    tmid = Column(Integer, ForeignKey("api_tm_list.tmid"), primary_key=True)
    start_date = Column(Date)
    stop_date = Column(Date)
    domainid = Column(Integer, ForeignKey("api_domains.domainid"), primary_key=True)
    servid = Column(Integer, ForeignKey("api_services.servid"), primary_key=True)
    daytype = Column(Integer)
    tstart = Column(Integer)
    tend = Column(Integer)
    mask = Column(String(250), ForeignKey("api_masks.mask"), primary_key=True)
    tdid = Column(Integer, ForeignKey("api_traf_dest.tdid"))
    cost = Column(Float)
    round0 = Column(Integer)
    round1 = Column(Integer)
    roundn = Column(Integer)
    operid = Column(Integer, ForeignKey("api_operators.operid"))
    make_date = Column(Date)
    mspid = Column(Integer)

    service = ''
    domain = ''
    tm = ''
    tpt = ''
    oper = ''
    tdval = ''

    def __repr__(self):
        row_str = '[tmid:%d][servid:%d][domainid:%d] [tdid:%s]%s (%s-%s) [%d:%d:%d] %s' % (
            self.tmid,
            self.servid,
            self.domainid,
            str(self.tdid),
            self.tdval,
            str(self.start_date),
            str(self.stop_date),
            self.daytype,
            self.tstart,
            self.tend,
            str(self.cost)
        )
        return row_str.encode('utf-8')
