# -*- coding: utf-8 -*-
import models
#from addons_mglife.data_sync.models.profiles import Profiles

class Syncer():

    def __init__(self, profile):
        self.profile = profile

    def process(self):
        '''
            Найти все мапы
            по всем мапам найти все правила
            если правил нет, смотреть дефолтные правила для типа объекта
            по всем найденным правилам найти привязанные шаблоны
            если привязанных шаблонов нет, найти дефолтные
            по всем найденным шаблонам подставить параметры и значения из объектов
            вернуть результирующий текст
        :return:
        '''
        pass

if __name__ == '__main__':
    print 'Test'
    prof = Profiles()
    print prof
