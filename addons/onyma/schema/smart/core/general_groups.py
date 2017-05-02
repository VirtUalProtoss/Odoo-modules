# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class GeneralGroups(Base):
    __tablename__ = 'general_groups'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("core.general_groups.id"))

    parent = relationship('GeneralGroups', backref='childrens', remote_side=id, foreign_keys=[parent_id,])

    def __repr__(self):
        return ("[%d]%s" % (self.id, self.name, )).encode('utf-8')
