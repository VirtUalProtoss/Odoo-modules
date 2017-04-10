# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *

from ...schema.onyma.apibilltype import ApiBillType
from .apiservices import ApiServices


class ApiMonthBills(Base):

    __tablename__ = 'api_month_bills'

    dmid = Column(Integer)
    mdate = Column(Date)
    ntype = Column(Integer, ForeignKey("api_bill_type.ntype"))
    servid = Column(Integer, ForeignKey('api_services.servid'))
    dogid = Column(Integer, ForeignKey("api_dog_list.dogid"))
    use = Column(Float)
    cost = Column(Float)
    amount = Column(Float)
    tmid = Column(Integer, ForeignKey('api_tm_list.tmid'))
    gid = Column(Integer) #ForeignKey("api_groups.gid"),
    use1 = Column(Float)
    bcid = Column(Integer) #ForeignKey("api_bill_type_class.bcid"),
    remark = Column(String(250))
    mbid = Column(Integer, primary_key=True)

    ntype_obj = relation(ApiBillType, primaryjoin=(ntype == ApiBillType.ntype))
    service = relationship(ApiServices)

    def __repr__(self):
        return ('[%d] [%d]%s %s %d %d %s %s %f %f' % (
            self.dogid,
            self.ntype,
            self.ntype_obj.remark,
            self.service.servname,
            self.bcid,
            self.gid,
            str(self.mdate),
            self.remark,
            self.use,
            self.amount,
        )).encode('utf-8')
