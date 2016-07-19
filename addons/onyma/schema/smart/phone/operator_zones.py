# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .operator_plists import OperatorPlists
from .operator_services import OperatorServices


class OperatorZones(Base):
    __tablename__ = 'operator_zones'

    __table_args__ = {'extend_existing': True, 'schema':'phone', }

    id = Column(Integer, primary_key=True)
    price_list_id = Column(Integer, ForeignKey("phone.operator_plists.id"))
    service_id = Column(Integer, ForeignKey("phone.operator_services.id"))
    who_pays = Column(Integer)
    price = Column(Float)
    protect = Column(Integer, nullable=False)
    start_rounding = Column(Integer)
    rounding = Column(Integer)
    use_prefixes = Column(Boolean)
    comments = Column(String)

    price_list = relation(OperatorPlists, primaryjoin=(price_list_id == OperatorPlists.id))
    service = relation(OperatorServices, primaryjoin=(service_id == OperatorServices.id))


    def __repr__(self):
        return ("[%d][%d][%d]%s: %s %s" % (
            self.id,
            self.service_id,
            self.price_list.operator_obj.id,
            self.price_list.operator_obj.name,
            self.service.name,
            str(self.price), )
        ).encode('utf-8')
