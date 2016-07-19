# -*- coding: utf-8 -*-

__author__ = 'virtual'

from billing.smart.oa import OA
from schema.smart.phone.users import Users

class Phone(OA):

    def __init__(self, session):
        OA.__init__(self, session)

    def get_phone(self, number):
        return self.get_table_data(Users, {'real_start_num' : number, })

    def get_phones(self):
        return self.get_table_data(Users)

    def get_phone_by_user(self, user):
        return self.get_table_data(Users, {'user_id' : user.id, })

    def get_phones_by_ls(self, lschet):
        accounts = self.get_oa_by_ls(lschet)
        phone_list = []
        for account in accounts:
            users = self.get_account_user(account)
            for user in users:
                phones = self.get_phone_by_user(user)
                for phone in phones:
                    phone_list.append(phone)
        return phone_list

    def get_ls_list(self):
        ls_list = []
        q = self.session.query(Users)
        phones = q.all()
        for phone in phones:
            account = phone.user.account.parent.account_number
            if account not in ls_list:
                ls_list.append(account)
        return ls_list
