# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *


class ApiAuditClientServices(Base):

    __tablename__ = 'api_audit_clientservices'

    clsrv = Column(Integer, ForeignKey("api_client_resources.id"))
    dmid = Column(Integer, ForeignKey("api_map_main.dmid"))
    service = Column(Integer, ForeignKey("api_resources.id"))
    tmid = Column(Integer, ForeignKey("api_tm_list.tmid"))
    startdate = Column(Date)
    enddate = Column(Date)
    ssdate = Column(Date)
    closed = Column(Integer)
    gid = Column(Integer, ForeignKey("api_groups.gid"), primary_key=True)
    dadd = Column(Date)
    oper = Column(Integer, ForeignKey("api_operators.operid"), primary_key=True)

    def get_status_name(self):
        statuses = {
            -1: {'name': 'not found', },
            0: {'name': 'active', },
            1: {'name': 'inactive', },
            2: {'name': 'paused by system', },
            3: {'name': 'paused by operator', },
            4: {'name': 'deleted', },
        }
        if not self.enddate: enddate = '...'
        else: enddate = self.enddate.strftime('%d.%m.%Y %H:%M:%S')

        return statuses[self.closed]['name'] + '(%s-%s)' % (
            self.startdate.strftime('%d.%m.%Y %H:%M:%S'),
            enddate,
        )

    def __repr__(self):
        return "[%d]%s" % (self.closed, self.get_status_name(), )
