# -*- coding: utf-8 -*-

__author__ = 'virtual'

from billing.smart import Smart
from schema.smart.core.accounts import Accounts
from schema.smart.core.accounts import Accounts as Parents
from schema.smart.core.users import Users
from schema.smart.phone.users import Users as PhoneUsers

from sqlalchemy import or_


class Dog(Smart):

    def __init__(self, session):
        Smart.__init__(self, session)

    def get_dogs(self, params={}):
        q = self.session.query(Accounts)
        q = q.join(Users)
        q = q.join(PhoneUsers)
        q = q.join(Accounts.parent, aliased=True)
        try:
            q = self.get_parametrized_filter(Accounts, q, params)
        except:
            pass
        try:
            q = self.get_parametrized_filter(Users, q, params)
        except:
            pass
        try:
            q = self.get_parametrized_filter(PhoneUsers, q, params)
        except:
            pass
        return q.all()

    def get_phones(self, params={}):
        q = self.session.query(PhoneUsers)
        q = q.join(Users)
        q = q.join(Accounts)
        q = q.join(Accounts.parent, aliased=True)
        try:
            q = self.get_parametrized_filter(Accounts, q, params)
        except:
            pass
        try:
            q = self.get_parametrized_filter(Users, q, params)
        except:
            pass
        try:
            q = self.get_parametrized_filter(PhoneUsers, q, params)
        except:
            pass
        return q.all()
