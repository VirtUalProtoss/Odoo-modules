# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .persons import Persons


class PersonInfos(Base):
    __tablename__ = 'person_infos'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    second_name = Column(String)
    last_name = Column(String)
    person_id = Column(Integer, ForeignKey("core.persons.id"))
    #service_type = Column(Integer)
    #service_sub_type = Column(Integer)

    person = relation(Persons, primaryjoin=(person_id == Persons.id), backref='info')

    def __repr__(self):
        return ("[%d] %s %s %s" % (self.id, self.first_name, self.second_name, self.last_name, )).encode('utf-8')
