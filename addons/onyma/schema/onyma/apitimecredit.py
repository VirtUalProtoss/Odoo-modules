# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *

from .apioperators import ApiOperators
from .apidoglist import ApiDogList


class ApiTimeCredit(Base):

    __tablename__ = 'api_time_credit'

    mdate = Column(Date)
    enddate = Column(Date)
    amount = Column(Float)
    dogid = Column(Integer, ForeignKey("api_dog_list.dogid"), primary_key=True)
    remark = Column(String(2000))
    operid = Column(Integer, ForeignKey("api_operators.operid"), primary_key=True)

    operator = relation(ApiOperators, primaryjoin=(operid == ApiOperators.operid))
    account = relation(ApiDogList, primaryjoin=(dogid == ApiDogList.dogid))

    def __getattr__(self, item):
        if type(item) == unicode:
            return item.encode('utf-8')
        else:
            return item

    def __repr__(self):
        return ('[%d] %s %s %s %f' % (
            int(self.dogid),
            str(self.mdate),
            self.remark,
            self.operator.name,
            float(self.amount),
        )).encode('utf-8')
