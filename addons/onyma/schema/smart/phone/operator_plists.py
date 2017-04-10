# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .operators import Operators


class OperatorPlists(Base):
    __tablename__ = 'operator_plists'

    __table_args__ = {'extend_existing': True, 'schema':'phone', }

    id = Column(Integer, primary_key=True)
    operator = Column(Integer, ForeignKey("phone.operators.id"))
    start_date = Column(DateTime)
    comments = Column(String)
    end_date = Column(DateTime)

    operator_obj = relation(Operators, primaryjoin=(operator == Operators.id))


    def __repr__(self):
        return ("[%d]%s: %s-%s" % (self.id, self.operator_obj.name,  self.start_date, str(self.end_date), )).encode('utf-8')
