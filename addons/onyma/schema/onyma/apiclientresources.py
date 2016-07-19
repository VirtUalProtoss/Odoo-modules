# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *
from ...schema.onyma.apidoglist import ApiDogList
from ...schema.onyma.apigroups import ApiGroups
from ...schema.onyma.apiresources import ApiResources
from ...schema.onyma.apitmlist import ApiTmList
from ...schema.onyma.apimapmain import ApiMapMain

statuses = {
    -1: {'name': 'not found', 'ru': 'Не найден', },
    0: {'name': 'active', 'ru': 'Активен', },
    1: {'name': 'inactive', 'ru': 'Неактивен', },
    2: {'name': 'paused by system', 'ru': 'Приостановлен системой', },
    3: {'name': 'paused by operator', 'ru': 'Приостановлен оператором', },
    4: {'name': 'deleted', 'ru': 'Удален', },
}


class ApiClientResources(Base):

    __tablename__ = 'api_client_resources'

    id = Column(Integer, primary_key=True)
    dogid = Column(Integer, ForeignKey("api_dog_list.dogid"))
    gid = Column(Integer, ForeignKey("api_groups.gid"))
    service = Column(Integer, ForeignKey("api_resources.id"))
    name = Column(String(4000))
    tmid = Column(Integer, ForeignKey("api_tm_list.tmid"))
    dmid = Column(Integer, ForeignKey("api_map_main.dmid"))
    notes = Column(String(2000))
    status = Column(Integer)
    startdate = Column(Date)
    enddate = Column(Date)
    startdatetime = Column(DateTime)
    enddatetime = Column(DateTime)

    domainid = Column(Integer)
    prop_vals = {}

    #property = relationship('api_client_props')
    account = relation(ApiDogList, primaryjoin=(dogid == ApiDogList.dogid))
    #properties = relationship('ApiClientProps', primaryjoin=(id == 'ApiClientProps.clsrv'), foreign_keys=['ApiClientProps.clsrv',])

    def get_status(self):
        return statuses[self.status]['ru']

    def get_property_value(self, property):
        if property not in self.prop_vals:
            for prop in self.properties:
                if prop.property == property:
                    self.prop_vals[property] = prop.value
        return self.prop_vals[property]

    def __repr__(self):
        return ('[%d]%s' % (self.id, self.name, )).encode('utf-8')
