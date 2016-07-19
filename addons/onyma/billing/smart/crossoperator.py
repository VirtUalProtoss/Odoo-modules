# -*- coding: utf-8 -*-

__author__ = 'virtual'

from billing.smart import Smart
from schema.smart.phone.operators import Operators
from schema.smart.phone.operator_plists import OperatorPlists
from schema.smart.phone.operator_services import OperatorServices
from schema.smart.phone.operator_zones import OperatorZones
from schema.smart.phone.prefixes import Prefixes
from schema.smart.phone.operator_zone_items import OperatorZoneItems

from sqlalchemy import or_


class CrossOperator(Smart):

    def __init__(self, session):
        Smart.__init__(self, session)

    def get_operators(self, params={}):
        q = self.session.query(Operators)
        q = self.get_parametrized_filter(Operators, q, params)
        return q.all()

    def get_operator_plists(self, operator, params={}):
        q = self.session.query(OperatorPlists)
        q = self.get_parametrized_filter(OperatorPlists, q, params)
        q = q.filter(OperatorPlists.operator==operator.id)
        return q.all()

    def get_plist_services(self, plist, params={}):
        q = self.session.query(OperatorZones)
        q = q.filter(OperatorZones.price_list_id==plist.id)
        q = self.get_parametrized_filter(OperatorZones, q, params)
        return q.all()

    def get_zone_ranges(self, zone, params={}):
        q = self.session.query(OperatorZoneItems)
        q = q.join(Prefixes)
        if len(params) > 0:
            if 'end_date' in params:
                q = q.filter(or_(Prefixes.end_date>=params['end_date'], Prefixes.end_date==None))
                del params['end_date']
            q = self.get_parametrized_filter(Prefixes, q, params)
        q = q.filter(OperatorZoneItems.zone_id==zone.id)
        return q.all()
