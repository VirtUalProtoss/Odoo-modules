# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiAuditDogList(Base):

    __tablename__ = 'api_audit_dog_list'

    bill = Column(Integer, ForeignKey("api_bill_list.bill"), primary_key=True)
    dogid = Column(Integer, ForeignKey("api_dog_list.dogid"), primary_key=True)
    gid = Column(Integer, ForeignKey("api_groups.gid"), primary_key=True)
    status = Column(Integer)
    startdate = Column(Date)
    enddate = Column(Date)
    status_date = Column(Date)
    auditmdate = Column(Date)
    auditoperid = Column(Integer, ForeignKey("api_operators.operid"), primary_key=True)
