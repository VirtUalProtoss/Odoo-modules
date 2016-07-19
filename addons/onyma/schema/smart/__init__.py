# -*- coding: utf-8 -*-

__author__ = 'virtual'


statuses = {
    None: {'name': 'None', },
    -1: { 'name': 'unknown', },
    0: { 'name': '',},
    1: { 'name': 'Новый',},
    2: { 'name': '',},
    3: { 'name': 'Активный', },
    4: { 'name': 'Приостановленный',},
    5: { 'name': 'Заблокированный', },
    6: { 'name': 'Удаленный', },
    7: { 'name': 'Закрытый', },
    8: { 'name': '', },
}

def get_status_name(status):
    return '[%d]%s' % (status, statuses[status]['name'], )
