# -*- coding: utf-8 -*-

__author__ = 'virtual'

from ...schema import *

from ...schema.onyma.apioperators import ApiOperators
from ...schema.onyma.apibilltype import ApiBillType
from ...schema.onyma.apidoglist import ApiDogList


bcid_operator = {
    0: 'default',
    24: 'МР Спарк',
    23: 'ТрансТелеКом',
    25: 'МР Кавказ',
    22: 'Ростелеком',
    29: 'Ростелеком Зона',
    27: 'Вымпелком',
    26: 'Кубтелеком',
}


class ApiBills(Base):

    __tablename__ = 'api_bills'

    bill = Column(Integer, primary_key=True) #ForeignKey("api_bill_list.bill"),
    mdate = Column(Date)
    amount = Column(Float)
    ntype = Column(Integer, ForeignKey("api_bill_type.ntype"), primary_key=True)
    service_money = Column(Integer, primary_key=True) #ForeignKey("api_currency_list.currencyid"),
    dogid = Column(Integer, ForeignKey("api_dog_list.dogid"), primary_key=True)
    gid = Column(Integer, primary_key=True) #ForeignKey("api_groups.gid"),
    billid = Column(Integer, primary_key=True)
    remark = Column(String(2000))
    operid = Column(Integer, ForeignKey("api_operators.operid"), primary_key=True)
    bcid = Column(Integer, primary_key=True) #ForeignKey("api_bill_type_class.bcid"),

    operator = relation(ApiOperators, primaryjoin=(operid == ApiOperators.operid))
    ntype_obj = relation(ApiBillType, primaryjoin=(ntype == ApiBillType.ntype))
    account = relation(ApiDogList, primaryjoin=(dogid == ApiDogList.dogid))

    def __getattr__(self, item):
        if type(item) == unicode:
            return item.encode('utf-8')
        else:
            return item

    def get_kassa_str(self):
        if self.remark:
            remark = self.remark.encode('utf-8')
        else:
            remark = ''
        oper = self.operator.name.encode('utf-8')
        return ('%s %s %s %s %s %s' % (
            self.mdate.strftime('%d.%m.%Y'),
            (str(round(self.amount, 2)) + ' руб.'),
            self.ntype_obj.remark.encode('utf-8'),
            bcid_operator[self.bcid],
            remark,
            oper,
        ))

    def __repr__(self):
        return ('[%d:%d] [%d]%s %d %d %s %s %s %f' % (
            self.bill,
            self.dogid,
            self.ntype,
            self.ntype_obj.remark,
            self.bcid,
            self.gid,
            str(self.mdate),
            self.remark,
            self.operator.name,
            self.amount,
        )).encode('utf-8')

    def getHtml(self):
        oper = self.operator.name
        mdate = self.mdate.strftime('%d.%m.%Y')
        hstr = '''
            <td>%s</td>
            <td>%s</td>
            <td>%f</td>
        ''' % (
            oper,
            mdate,
            self.amount,
        )
        return hstr
