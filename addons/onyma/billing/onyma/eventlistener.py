# -*- coding: utf-8 -*-

__author__ = 'virtual'

from . import Onyma
from datetime import datetime
from schema.openmn.resourcestatus import ResourceStatus


class EventListener(Onyma):

    def __init__(self, session):
        Onyma.__init__(self, session)

    def get_resource_changes(self, params={}, c_date=datetime.now()):
        q = self.session.query(ResourceStatus)
        #q = q.filter(ResourceStatus.update_time >= c_date)
        q = self.get_parametrized_filter(ResourceStatus, q, params)
        return q.all()

    def update_change(self, gid, clsrv_list, res_id_list, process_time=datetime.now(), commit=True):
        stmt = ResourceStatus.__table__.update()\
        .where(ResourceStatus.std_eps_gid==gid)\
        .where(ResourceStatus.resource_type.in_(res_id_list))\
        .where(ResourceStatus.processed_time==None)\
        .where(ResourceStatus.p_clsrv.in_(clsrv_list))\
        .values(processed_time=process_time)

        self.session.execute(stmt)
        if commit:
            self.session.commit()
        else:
            self.session.rollback()
