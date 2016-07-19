__author__ = 'virtual'

from ...schema import *
from ..onyma import *


class ApiTrafDestD(Base):

    __tablename__ = 'api_traf_dest_d'

    tdid = Column(Integer, primary_key=True)
    tdup = Column(Integer, ForeignKey("api_traf_dest_d.tdid"))

    tdname = Column(String(255))
    tdval = Column(String(128))
    traftype = Column(Integer)
    tzid = Column(Integer)
    zone = Column(Integer)

    def __repr__(self):
        row_str = "%s %s %s %s %s %s %s" % (
            self.tdid,
            self.tdup,
            self.tdname,
            self.tdval,
            self.traftype,
            self.tzid,
            self.zone,
        )
        return row_str.encode('utf-8')
