# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiClsrvStatusHistory(Base):

    __tablename__ = 'api_clsrv_status_history'

    sid = Column(Integer, primary_key=True)
    status = Column(Integer, primary_key=True)
    sdate = Column(Date, primary_key=True)
    edate = Column(Date, primary_key=True)
    service = Column(Integer, primary_key=True)
    gid = Column(Integer)
    name = Column(String(4000))

    def get_status_name(self):
        statuses = {
            -1: {'name': 'not found', },
            0: {'name': 'active', },
            1: {'name': 'inactive', },
            2: {'name': 'paused by system', },
            3: {'name': 'paused by operator', },
            4: {'name': 'deleted', },
        }
        if not self.edate: edate = '...'
        else: edate = self.edate.strftime('%d.%m.%Y %H:%M:%S')

        return statuses[self.status]['name'] + '(%s-%s)' % (
            self.sdate.strftime('%d.%m.%Y %H:%M:%S'),
            edate,
        )

    def __repr__(self):
        return "[%d]%s" % (self.status, self.get_status_name(), )
