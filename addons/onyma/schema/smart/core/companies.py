# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class Companies(Base):
    __tablename__ = 'companies'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)

    parent_id = Column(Integer, ForeignKey("core.companies.id"))
    agent_id = Column(Integer, ForeignKey("core.companies.id"))
    name = Column(String)
    status = Column(Integer)

    parent = relationship('Companies', remote_side=id, backref='children', foreign_keys=[parent_id,])
    agent = relationship('Companies', remote_side=id, foreign_keys=[agent_id,])

    def __repr__(self):
        return "[%d=>%d]%s %d"% (self.id, self.parent_id, self.name, self.status, )
