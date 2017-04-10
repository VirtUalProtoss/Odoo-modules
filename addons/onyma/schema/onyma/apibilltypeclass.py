__author__ = 'virtual'

from ...schema import *
from ...schema.onyma import *


class ApiBillTypeClass(Base):

    __tablename__ = 'api_bill_type_class'

    bcid = Column(Integer, primary_key=True)
    name = Column(String(255))
    gid = Column(Integer)

    def __repr__(self):
        row_str = "[%d]%s" % (
            self.bcid,
            self.name,
        )
        return row_str.encode('utf-8')
