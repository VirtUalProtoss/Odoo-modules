# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from schema.smart import get_status_name
from .accounts import Accounts

class AccountStatuses(Base):
    __tablename__ = 'account_statuses'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("core.accounts.id"))
    status = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    account = relation(Accounts, primaryjoin=(account_id == Accounts.id))
    #account = relationship('Accounts', remote_side=id, backref='account_status')

    #def get_l_date(self, field):
    #    return pytz.UTC.localize(self.__dict__[field])

    def __repr__(self):
        return "[%d]%s" % (self.status, self.get_status_name(), )

    def get_status_name(self):
        if not self.end_date:
            end_date = '...'
        else:
            end_date = self.end_date.strftime('%d.%m.%Y %H:%M:%S')
        return get_status_name(self.status) + ' (%s-%s)' % (
            self.start_date.strftime('%d.%m.%Y %H:%M:%S'),
            end_date,
        )
