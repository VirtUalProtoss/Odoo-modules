# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .operators import Operators


class Prefixes(Base):
    __tablename__ = 'prefixes'

    __table_args__ = {'extend_existing': True, 'schema':'phone', }

    id = Column(Integer, primary_key=True)
    prefix = Column(String)
    is_empty_prefix = Column(Boolean, nullable=False)
    trunk1 = Column(String)
    trunk2 = Column(String)
    trunk3 = Column(String)
    empty_condition = Column(Integer)
    operator_id = Column(Integer, ForeignKey('phone.operators.id'))
    associate_op_id = Column(Integer, ForeignKey('phone.associate_ops.id'))
    exchange_id = Column(Integer, ForeignKey('phone.exchanges.id'))
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    operator = relation(Operators, primaryjoin=(operator_id == Operators.id))

    def range(self):
        p_len = len(self.prefix)
        return {
            'from': self.prefix + ('0' * (11 - p_len)),
            'to': self.prefix + ('9' * (11 - p_len)),
        }

    def __repr__(self):
        range = self.range()
        return ("[%d]%s: %s %s (%s-%s)" % (
                self.id,
                self.prefix,
                self.start_date,
                str(self.end_date),
                range['from'],
                range['to'],
            )
        ).encode('utf-8')
