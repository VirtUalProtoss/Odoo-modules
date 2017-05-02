# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
#from ..core.users import Users as CUsers


class Users(Base):
    __tablename__ = 'users'

    __table_args__ = {'extend_existing': True, 'schema':'phone', }

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("core.users.id"))
    real_start_num = Column(String(50))
    real_end_num = Column(String(50))

#    user = relation(CUsers, primaryjoin=(user_id == CUsers.id))


    def __repr__(self):
        return "%s: [%d]%s-%s" % (self.user.account.get_parent().account_number, self.id, self.real_start_num, self.real_end_num, )
