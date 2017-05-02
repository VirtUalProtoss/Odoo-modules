# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *


class X07_SRV_DCT(Base):

    __tablename__ = 'X07_SRV_DCT'

    srv_id = Column(Integer, primary_key=True)
    srv_key = Column(String(10))
    srv_name = Column(String(400))
    srv_shortname = Column(String(200))
    subservice_id = Column(Integer, ForeignKey('SUBSERVICE_T.subservice_id'))

    def __repr__(self):

        return ('[%d][%d](%s) %s %s' % (
            self.srv_id,
            self.subservice_id,
            self.srv_key,
            self.srv_shortname,
            self.srv_name,
        )).encode('utf-8')
