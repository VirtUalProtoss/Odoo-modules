# -*- coding: utf-8 -*-

__author__ = 'virtual'

from schema import *
from .users import Users
from .persons import Persons
from .companies import Companies
from .generalgr_links import GeneralGrLinks
from datetime import datetime


class Accounts(Base):
    __tablename__ = 'accounts'

    __table_args__ = {'extend_existing': True, 'schema':'core', }

    current_status = None

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("core.accounts.id"))
    base_account_id = Column(Integer, ForeignKey("core.accounts.id"))
    person_id = Column(Integer, ForeignKey("core.persons.id"))
    company_id = Column(Integer, ForeignKey("core.companies.id"))
    base_company_id = Column(Integer, ForeignKey("core.companies.id"))
    account_number = Column(String)
    balance = Column(Float)
    child_balance = Column(Float)
    type = Column(Integer)

    parent = relationship('Accounts', backref='childrens', remote_side=id, foreign_keys=[parent_id,])
    base_account = relationship('Accounts', remote_side=id, foreign_keys=[base_account_id,])
    #parent = relation('Accounts', primaryjoin=(parent_id == id))
    users = relationship(Users) #, remote_side=id, backref='account')
    statuses = relationship('AccountStatuses') #, remote_side=account_id, backref='account')
    person = relationship(Persons)
    company = relationship(Companies, foreign_keys=[company_id,])
    base_company = relationship(Companies, foreign_keys=[base_company_id,])
    general_groups = relationship(GeneralGrLinks, backref='account')

    def get_group_str(self):
        groups = self.get_group_list()
        if groups:
            return ', '.join(groups)
        else:
            return ''

    def get_acc_type(self):
        if self.parent:
            if self.parent.person:
                return 'fl'
            if self.parent.company:
                return 'yl'
        else:
            if self.person:
                return 'fl'
            if self.company:
                return 'yl'

    def get_client_name(self):
        if self.parent:
            if self.parent.person:
                return self.parent.person.name
            if self.parent.company:
                return 'yl'
        else:
            if self.person:
                return 'fl'
            if self.company:
                return 'yl'

    def get_group_list(self):
        groups = []
        if self.general_groups and len(self.general_groups) > 0:
            for group in self.general_groups:
                groups.append(group.group.name)
        return groups

    def check_group_match(self, group_name):
        if group_name.decode('utf-8') in self.get_group_list():
            return True
        else:
            return False

    def get_status_list(self, c_date=datetime.now()):
        check_statuses = []
        curr_status = None
        # Выбираем только статусы в диапазоне дат с c_date по текущее число
        for status in self.statuses:
            if not status.start_date:
                continue
            if (not status.end_date or status.end_date.timetuple() >= c_date.timetuple()) \
                    and (status.start_date.timetuple() <= c_date.timetuple()):
                # Статус на границе c_date
                check_statuses.append(status)
            elif status.start_date.timetuple() >= c_date.timetuple():
                # Вся история статусов начиная с c_date
                check_statuses.append(status)

            if not status.end_date:
                # И отдельно последний статус
                curr_status = status

        if not self.current_status:
            self.current_status = curr_status
        # Сортируем список статусов по убыванию
        sorted_statuses = [(a.start_date.toordinal(), a) for a in check_statuses]
        sorted_statuses.sort()
        check_statuses = [b[1] for b in sorted_statuses]

        return curr_status, check_statuses

    def get_status(self, c_date=datetime.now()):
        if 'current_status' not in self.__dict__ or not self.current_status:
            self.get_status_list()
        return self.current_status

    def get_parent(self):
        return self.parent

    '''
    def __getattribute__(self, item):
        if item == 'current_status':
            if not self.current_status:
                self.get_status_list()
            return self.current_status
        elif item in self.__dict__:
            return self.__dict__[item]
        else:
            return None
    '''

    def __repr__(self):
        if not self.parent_id:
            parent_id = -1
        else:
            parent_id = self.parent_id
        return ("[%d=>%d] %s %s (%s)" % (self.id, parent_id, self.get_acc_type(), self.account_number, self.get_group_str(), )).encode('utf-8')
