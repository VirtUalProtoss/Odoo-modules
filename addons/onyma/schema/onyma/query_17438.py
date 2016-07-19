# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *

from .apidoglist import ApiDogList
from .apiclientresources import ApiClientResources
from ...billing.onyma import statuses


class UAPI_V_QUERY_17438(Base):

    __tablename__ = 'UAPI_V_QUERY_17438'

    f1 = Column(Integer, ForeignKey("api_client_resources.id"), primary_key=True) # clsrv
    f3 = Column(Integer, ForeignKey("api_dog_list.dogid"), primary_key=True) # dogid
    f4 = Column(String) # phone_number
    f2 = Column(Integer) # status

    dogovor = relation(ApiDogList, primaryjoin=(f3 == ApiDogList.dogid))
    clsrv_obj = relation(ApiClientResources, primaryjoin=(f1 == ApiClientResources.id))

    def get_kassa_str(self):
        return ('%s %s' % (
            self.f4,
            statuses[self.f2]['ru'].decode('utf-8'),
        )).encode('utf-8')

    def __repr__(self):
        return ('[%d:%d] [%d]%s' % (
            self.f1,
            self.f3,
            self.f2,
            self.f4,
        )).encode('utf-8')
