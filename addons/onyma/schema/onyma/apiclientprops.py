__author__ = 'virtual'

from ...schema import *
from ...schema.onyma import *
from .apiclientresources import ApiClientResources


class ApiClientProps(Base):

    __tablename__ = 'api_client_props'

    id = Column(Integer, primary_key=True)
    clsrv = Column(Integer, ForeignKey("api_client_resources.id"))
    property = Column(Integer, ForeignKey("api_props.id"))
    value_num = Column(Integer)
    value = Column(String(4000))
    real_value = Column(String(2000))
    value_type = Column(String(3))
    status = Column(Integer)
    parentclsrv = Column(Integer, ForeignKey("api_client_resources.id"))
    gid = Column(Integer)

    clsrv_obj = relationship(ApiClientResources, foreign_keys=[clsrv,], backref='properties')
    parentclsrv_obj = relationship(ApiClientResources, foreign_keys=[parentclsrv,])
    #clsrv_obj = relation(ApiClientResources, primaryjoin=(clsrv == ApiClientResources.id), backref='properties')
    #parentclsrv_obj = relation(ApiClientResources, primaryjoin=(parentclsrv == ApiClientResources.id))

    def __repr__(self):
        row_str = "[%d:%d]%s %s" % (
            self.clsrv,
            self.property,
            self.value,
            self.real_value,
        )
        return row_str.encode('utf-8')
