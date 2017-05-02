# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class ResourceStatus(Base):
    __tablename__ = 'resource_status'

    __table_args__ = {'extend_existing': True, 'schema':'public', }

    p_status = Column(Integer)
    p_clsrv = Column(Integer, primary_key=True)
    p_old_status = Column(Integer)
    std_eps_gid = Column(Integer)
    p_prop_message = Column(Integer)

    update_time = Column(DateTime)
    processed_time = Column(DateTime)
    resource_type = Column(Integer)
    serialize = Column(String)


    def __repr__(self):
        if self.processed_time:
            proc_time = self.processed_time.strftime('%Y%m%d %H:%M%S.%s')
        else:
            proc_time = ' ... '
        return "[%d:%d:%d][%d=>%d] %d (%s - %s)" % (
            self.std_eps_gid,
            self.resource_type,
            self.p_clsrv,
            self.p_old_status,
            self.p_status,
            self.p_prop_message,
            self.update_time.strftime('%Y-%m-%d %H:%M:%S.%s'),
            proc_time,
        )
