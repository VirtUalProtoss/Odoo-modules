__author__ = 'virtual'

from ...schema import *
from ...schema.onyma import *
from .apiclientresources import ApiClientResources

class ApiBillType(Base):

    __tablename__ = 'api_bill_type'

    ntype = Column(Integer, primary_key=True)
    remark = Column(String(100))
    gid = Column(Integer)
    service_money = Column(Integer)
    deb_cred = Column(Integer)

    def __repr__(self):
        row_str = "[%d]%s" % (
            self.ntype,
            self.remark,
        )
        return row_str.encode('utf-8')
