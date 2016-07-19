# -*- coding: utf-8 -*-

__author__ = 'virtual'

from sqlalchemy import not_

'''
    Высокоуровненвые схемы биллингов, используют низкоуровневые схемы.
    Единый интерфейс для абстракции данных биллингов.
'''


class Billing():

    error_sql = '''
        select err.get_error_message from dual
    '''

    def __init__(self, session):
        self.session = session #.get_session()
        self.db_conn = session

    def auth(self, schema):
        self.db_conn.auth()

    def get_parametrized_filter(self, table, query, params):
        for param in params:
            try:
                if type(params[param]) == dict:
                    if 'check_type' in params[param]:
                        value = params[param]['value']
                        if type(value) == str or type(value) == unicode:
                            if value.find('(') > -1:
                                value = eval(value)

                        ct = params[param]['check_type']
                        if ct == '>' or ct == 'gt':
                            query = query.filter(table.__dict__[param]>value)
                        elif ct == '>=' or ct == 'gte':
                            query = query.filter(table.__dict__[param]>=value)
                        elif ct == '<' or ct == 'lt':
                            query = query.filter(table.__dict__[param]<value)
                        elif ct == '<=' or ct == 'lte':
                            query = query.filter(table.__dict__[param]==value)
                        elif ct == 'in':
                            query = query.filter(table.__dict__[param].in_(value))
                        elif ct == 'not in' or ct == 'not_in':
                            query = query.filter(not_(table.__dict__[param].in_(value)))
                        elif ct == 'not null' or ct == 'not_null':
                            query = query.filter(table.__dict__[param]!=None)
                        elif ct == '!=' or ct == 'not':
                            query = query.filter(table.__dict__[param]!=value)
                        elif not ct or ct == 'null':
                            query = query.filter(table.__dict__[param]==None)
                        elif ct == 'between':
                            query = query.filter(table.__dict__[param]>=value)
                            value2 = params[param]['value2']
                            query = query.filter(table.__dict__[param]<=value2)
                        elif ct == 'like':
                            query = query.filter(table.__dict__[param].like(value + '%'))
                else:
                    value = params[param]
                    if type(value) == str or type(value) == unicode:
                        value = value.decode('utf-8')
                        if value.find('(') > -1:
                            value = eval(value)
                    query = query.filter(table.__dict__[param]==value)
            except:
                continue

        return query

    def get_table_data(self, table, params={}):
        q = self.session.query(table)
        q = self.get_parametrized_filter(table, q, params)
        return q.all()

    def exec_function(self, func_name, params):
        return self.session.execute(func_name, params)

    def get_error_message(self):
        for row in self.session.execute(self.error_sql):
            print row[0]
