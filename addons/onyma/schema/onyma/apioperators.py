__author__ = 'virtual'

from .. import *
from ..onyma import *
from .apiclientresources import ApiClientResources

class ApiOperators(Base):

    __tablename__ = 'api_operators'

    operid = Column(Integer, primary_key=True)
    name = Column(String(250))
    login = Column(String(32))
    schema = Column(String(32))
    remark = Column(String(250))
    email = Column(String(250))
    cdate= Column(DateTime)
    edate= Column(DateTime)
    gid = Column(Integer)

    def __repr__(self):
        row_str = "[%d:%d]%s" % (
            self.gid,
            self.operid,
            self.name,
        )
        return row_str.encode('utf-8')
