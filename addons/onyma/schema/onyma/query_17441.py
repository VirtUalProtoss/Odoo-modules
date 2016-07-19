# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *

from .apidoglist import ApiDogList


class UAPI_V_QUERY_17441(Base):

    __tablename__ = 'UAPI_V_QUERY_17441'

    f1 = Column(Integer, ForeignKey("api_dog_list.dogid"), primary_key=True) # dogid
    f2 = Column(Integer) # utid
    f3 = Column(String(2)) # ctype
    f4 = Column(String) # vdog
    f5 = Column(String) # client

    dogovor = relation(ApiDogList, primaryjoin=(f1 == ApiDogList.dogid))

    def __repr__(self):
        return ('[%d:%d] %s %s %s' % (
            self.f1,
            self.f2,
            self.f3,
            self.f4,
            self.f5,
        )).encode('utf-8')
