# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class OperatorServices(Base):
    __tablename__ = 'operator_services'

    __table_args__ = {'extend_existing': True, 'schema':'phone', }

    id = Column(Integer, primary_key=True)
    name = Column(String)
    comments = Column(String)
    status = Column(Integer)
    create_date = Column(DateTime)

    def __repr__(self):
        return "[%d]%s: %s" % (self.id, self.name,  self.create_date, )
