# -*- coding: utf-8 -*-

__author__ = 'virtual'

from .. import Billing
from ...schema.onyma.apioperators import ApiOperators


statuses = {
    -1: {'name': 'not found', 'ru': 'Не найден', },
    0: {'name': 'active', 'ru': 'Активен', },
    1: {'name': 'inactive', 'ru': 'Неактивен', },
    2: {'name': 'paused by system', 'ru': 'Приостановлен системой', },
    3: {'name': 'paused by operator', 'ru': 'Приостановлен оператором', },
    4: {'name': 'deleted', 'ru': 'Удален', },
}


class Onyma(Billing):

    def __init__(self, session):
        Billing.__init__(self, session)

    def get_operator_by_login(self, login):
        q = self.session.query(ApiOperators)
        q = q.filter(ApiOperators.login==login)

        return q.all()

    def get_operators_by_gid(self, gid):
        q = self.session.query(ApiOperators)
        q = q.filter(ApiOperators.gid == gid)

        return q.all()

    def fill_params(self, params):
        param_data = {}
        param_str = ''
        for param in params:
            if type(params[param]) == dict and 'check_type' in params[param]:
                check_type = params[param]['check_type']
                value = params[param]['value']
                #if type(value) == list:
                #    val_str = ''
                #    for el in value:
                #        val_str += str(el) + ', '
                #    value = '(' + val_str[:-2] + ')'
                if check_type == 'between':
                    value2 = params[param]['value2']
                    value = value + ' and ' + value2
            else:
                check_type = '='
                value = params[param]

            pparam = param.split('.')
            if len(pparam) > 1:
                sparam = pparam[1]
            else:
                sparam = pparam[0]
            param_str += ' and ' + param + ' ' + check_type + ' :' + sparam
            param_data.update({sparam: value, })
        #print param_str, param_data
        return param_str, param_data
