# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiDogList(Base):

    __tablename__ = 'api_dog_list'

    dogid = Column(Integer, primary_key=True)
    bill = Column(Integer, ForeignKey("api_bill_list.bill"))
    gid = Column(Integer, ForeignKey("api_groups.gid"))
    dogcode = Column(String(80))
    status = Column(Integer)
    startdate = Column(Date)
    enddate = Column(Date)
    status_date = Column(Date)
    tsid =	Column(Integer, ForeignKey("api_tax_sch.tsid"))
    csid =	Column(Integer, ForeignKey("api_credit_sch.csid"))
    utid =	Column(Integer, ForeignKey("api_user_type.utid"))

    statuses = {
        -1: {'name': 'not found', },
        0: {'name': 'active', },
        1: {'name': 'inactive', },
        2: {'name': 'paused by system', },
        3: {'name': 'paused by operator', },
        4: {'name': 'deleted', },
    }

    vdog = None

    def get_dog_type(self):
        if self.utid == 25:
            return 'ФЛ'
        elif self.utid == 26:
            return 'ЮЛ'
        else:
            return ''

    def get_cname_attr(self):
        if self.utid == 25:
            return 291
        elif self.utid == 26:
            return 12
        else:
            return None

    def __repr__(self):
        if not self.enddate:
            enddate = ' --- '
        else:
            enddate = self.enddate.strftime('%d.%m.%Y %H:%M:%S')
        startdate = self.startdate.strftime('%d.%m.%Y %H:%M:%S')
        rstr = ('''[%d]%s:[%d]%s (%s-%s)''' % (
            self.dogid,
            self.dogcode,
            self.status,
            self.statuses[self.status]['name'],
            startdate,
            enddate,
        )).encode('utf-8')
        return rstr
