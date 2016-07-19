__author__ = 'virtual'

from ...schema import *

from ...schema.onyma.apioperators import ApiOperators
from ...schema.onyma.apibilltype import ApiBillType
from ...schema.onyma.apibilltypeclass import ApiBillTypeClass
from ...schema.onyma.apidoglist import ApiDogList


class ApiDogpayment(Base):

    __tablename__ = 'api_dogpayment'

    billid = Column(Integer, primary_key=True)
    cdate = Column(Date)
    mdate = Column(Date)
    idate = Column(Date)
    billdate = Column(Date)
    amountr = Column(Float)
    amount = Column(Float)
    currencyid = Column(Integer, ForeignKey("api_currency_list.currencyid"))
    coef = Column(Integer)
    dogid = Column(Integer, ForeignKey("api_dog_list.dogid"))
    ntype = Column(Integer, ForeignKey("api_bill_type.ntype"))
    ppid = Column(String(250), ForeignKey("api_pay_point.ppid"))
    paydoc = Column(String(250))
    payed = Column(Integer)
    rmrk = Column(String(4000))
    operid = Column(Integer, ForeignKey("api_operators.operid"))
    bcid = Column(Integer, ForeignKey("api_bill_type_class.bcid"))
    ppdate = Column(Date)
    mamount = Column(Float)
    mcurrency = Column(Integer, ForeignKey("api_currency_list.currencyid"))
    load_id = Column(Integer)

    operator = relation(ApiOperators, primaryjoin=(operid == ApiOperators.operid))
    ntype_obj = relation(ApiBillType, primaryjoin=(ntype == ApiBillType.ntype))
    bcid_obj = relation(ApiBillTypeClass, primaryjoin=(bcid == ApiBillTypeClass.bcid))
    account = relation(ApiDogList, primaryjoin=(dogid == ApiDogList.dogid))
