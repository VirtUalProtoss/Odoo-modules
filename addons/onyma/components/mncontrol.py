# -*- encoding: utf-8 -*-

__author__ = 'virtual'

service_mod_params = {
    'on': {'params': [{'_key': 'activation', '_value': 'yes',}, {'_key': 'authorization', '_value': 'yes',},], },
    'off': {'params': [{'_key': 'activation', '_value': 'no',}, {'_key': 'authorization', '_value': 'no',},], },
}

class MNControl():

    def __init__(self):
        pass

    def set_connection(self, conn):
        self.__connection = conn

    def set_area_code(self, areaCode):
        self.areaCode = areaCode

    def getParamList(self, mn_params):
        params = {}
        for param in mn_params:
            params.update({
                param['_key']: param['_value'],
            })
        return params

    def getSubscriberSevices(self, number, svc=[]):
        subscriber = self.get_subscriber('supplementaryServiceSubscriber', number)

        if len(svc) > 0:
            subscriber.service = svc

        services = []
        mn_services = self.__connection.service.getSupplementaryServices(subscriber)
        for mn_service in mn_services:
            for service in mn_service[1]['service']:
                #print type(service), service
                services.append({
                    'oid': service['_oid'],
                    'params': self.getParamList(service['param']),
                })

        return services

    def get_subscriber(self, stype, number):
        subscriber = self.__connection.factory.create(stype)
        subscriber._areaCode = self.areaCode
        subscriber._dn = number
        return subscriber

    def getSubscriberSuspensionStatus(self, number):
        subscriber = self.get_subscriber('getSubscriberSuspensionStatus', number)
        subscriber._areaCode = self.areaCode
        subscriber._dn = number
        mn_status = self.__connection.service.getSubscriberSuspensionStatus(subscriber)
        status = ''
        category = 0
        val_type = ''
        for subscriber in mn_status:
            if subscriber[0] == 'error':
                status = {subscriber[0]: str(subscriber[1]), 'status': subscriber[0], }
            else:
                for param in subscriber[1]['param']:
                    if param['_key'] == 'status':
                        status = param['_value']
                    elif param['_key'] == 'supplSrvSetName':
                        category = param['_value']
                    elif param['_key'] == 'supplSrvSetId':
                        category = param['_value']
                    elif param['_key'] == 'type':
                        val_type = param['_value']
                    else:
                        pass
        return status, category, val_type

    def suspendPhone(self, number):
        subscriber = self.get_subscriber('modifySubscriberSuspension', number)

    def hold(self, number, category=5, status='suspend', val_type='out'):
        subscriber = self.get_subscriber('modifySubscriberSuspension', number)
        subscriber._status = status
        subscriber.param = [
            {'_key': 'supplSrvSetId', '_value': category, },
            {'_key': 'type', '_value': val_type, },
        ]
        self.__connection.service.modifySubscriberSuspension(subscriber)

    def remove(self, number, category=2):
        subscriber = self.get_subscriber('modifySubscriberSuspension', number)
        subscriber._status = 'suspend'
        subscriber.param = [
            {'_key': 'supplSrvSetId', '_value': category, },
            {'_key': 'type', '_value': 'out_inc', },
        ]
        self.__connection.service.modifySubscriberSuspension(subscriber)

    def hold_mgmn(self, number):
        subscriber = self.get_subscriber('modifySubscriberSuspension', number)
        subscriber._status = 'suspend'
        subscriber.param = [
            {'_key': 'supplSrvSetId', '_value': '4', },
            {'_key': 'type', '_value': 'out', },
        ]
        self.__connection.service.modifySubscriberSuspension(subscriber)

    def hold_mgmn_operator(self, number, operator):
        subscriber = self.get_subscriber('modifyParameters', number)
        #subscriber._status = 'suspend'
        subscriber.param = [
            {'_key': 'subscriberCategory', '_value': str(operator), },
        ]
        self.__connection.service.modifySubscriberParameters(subscriber)

    def unhold_mgmn_operator(self, number, operator):
        subscriber = self.get_subscriber('modifyParameters', number)
        subscriber._status = 'resume'
        subscriber.param = [
            {'_key': 'subscriberCategory', '_value': str(operator), },
        ]
        self.__connection.service.modifySubscriberParameters(subscriber)

    def unhold(self, number):
        subscriber = self.get_subscriber('modifySubscriberSuspension', number)
        subscriber._status = 'resume'
        self.__connection.service.modifySubscriberSuspension(subscriber)

    def unhold_mgmn(self, number):
        subscriber = self.get_subscriber('modifySubscriberSuspension', number)
        subscriber._status = 'resume'
        self.__connection.service.modifySubscriberSuspension(subscriber)

    def set_operator_mgmn(self, number, operator):
        '''
        <modifySubscriberParameters>
        <subscriber areaCode="8617" dn="670008">
        <param key="subscriberCategory" value="23"/>
        </subscriber>
        </modifySubscriberParameters>
        '''
        pass

    def set_add_service(self, number, service, params=[]):
        subscriber = self.get_subscriber('supplementaryServiceSubscriber', number)
        subscriber.service = service
        subscriber.service[0].update({'param': service_mod_params['on']['params'], })

        if len(params) > 0:
            for param in params:
                subscriber.service[0]['param'].append(param)

        return self.__connection.service.modifySupplementaryServices(subscriber)

    def set_del_service(self, number, service, params=[]):
        subscriber = self.get_subscriber('supplementaryServiceSubscriber', number)
        subscriber.service = service
        subscriber.service[0].update({'param': service_mod_params['off']['params'], })

        if len(params) > 0:
            for param in params:
                subscriber.service[0]['param'].append(param)

        return self.__connection.service.modifySupplementaryServices(subscriber)
