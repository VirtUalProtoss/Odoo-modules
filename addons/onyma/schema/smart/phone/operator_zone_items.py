# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .operator_zones import OperatorZones
from .prefixes import Prefixes

class OperatorZoneItems(Base):
    __tablename__ = 'operator_zone_items'

    __table_args__ = {'extend_existing': True, 'schema':'phone', }

    id = Column(Integer, primary_key=True)
    zone_id = Column(Integer, ForeignKey("phone.operator_zones.id"))
    prefix_id = Column(Integer, ForeignKey("phone.prefixes.id"))

    zone = relation(OperatorZones, primaryjoin=(zone_id == OperatorZones.id))
    prefix = relation(Prefixes, primaryjoin=(prefix_id == Prefixes.id))


    def __repr__(self):
        return "%s: %s" % (self.zone, self.prefix, )
