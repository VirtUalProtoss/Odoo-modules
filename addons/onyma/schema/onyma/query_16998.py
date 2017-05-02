# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *

from ..onyma.apidoglist import ApiDogList
from ..onyma.apibilltype import ApiBillType
from ..onyma.apibilltypeclass import ApiBillTypeClass
from .apitrafdestd import ApiTrafDestD
from .apiclientresources import ApiClientResources


class UAPI_V_QUERY_16998(Base):

    __tablename__ = 'UAPI_V_QUERY_16998'

    f1 = Column(DateTime, primary_key=True) # t1.USEDATE
    f2 = Column(String, primary_key=True) # substr(t1.REMARK, instr(t1.REMARK, '=', 1, 3)+ 6, length(t1.REMARK)- instr(t1.REMARK, '=', 1, 3)+ 6) num_a
    f3 = Column(String, primary_key=True) # substr(t1.COMMENTS, 7, length(t1.COMMENTS)- 5) num_b
    f4 = Column(Float, primary_key=True) # t1.USESERV
    f5 = Column(Float, primary_key=True) # t1.PCOST
    f6 = Column(Integer, primary_key=True) # t1.SPRES
    f7 = Column(Integer, primary_key=True) # t9.NTYPE
    f8 = Column(Integer, primary_key=True) # t9.BCID
    f9 = Column(Integer, primary_key=True) # t9.SGID
    f10 = Column(Integer, ForeignKey("api_dog_list.dogid"), primary_key=True) # t3.DOGID
    f11 = Column(Integer, primary_key=True) # t9.SERVID
    f12 = Column(Integer, primary_key=True) # t1.TDID
    f13 = Column(Integer, primary_key=True) # t1.res

    dogovor = relation(ApiDogList, foreign_keys=[f10,],primaryjoin=(f10 == ApiDogList.dogid))
    ntype_obj = relation(ApiBillType, foreign_keys=[f7,],primaryjoin=(f7 == ApiBillType.ntype))
    bcid_obj = relation(ApiBillTypeClass, foreign_keys=[f8,],primaryjoin=(f8 == ApiBillTypeClass.bcid))
    tpt = relation(ApiTrafDestD, foreign_keys=[f12,],primaryjoin=(f12 == ApiTrafDestD.tdid))
    clsrv = relation(ApiClientResources, primaryjoin=(f13 == ApiClientResources.id), foreign_keys=[f13,])
